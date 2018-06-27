from django.shortcuts import render_to_response, redirect, render, get_object_or_404
from django.template.context_processors import csrf
from django.http.response import HttpResponseBadRequest

from .utils import *
from .forms import *
from .models import *

from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

import datetime
import dateutil.parser
from dateutil.relativedelta import *


def login(request):
    context = {}
    context.update(csrf(request))

    if request.POST:
        try:

            username = request.POST.get('username', '')
            password = request.POST.get('password', '')

            user = auth.authenticate(username=username, password=password)

            if user is not None:
                auth.login(request, user)
                return redirect('index')

            else:
                context['login_error'] = "Wrong login or password"

        except():
            return HttpResponseBadRequest()

    return render_to_response('fantastical_things/login.html', context)


def logout(request):
    auth.logout(request)

    return redirect('login')


def registration(request):
    context = {}
    context.update(csrf(request))

    if request.POST:
        try:
            new_user_form = UserCreateForm(request.POST)

            if new_user_form.is_valid():
                new_user_form.save()
                new_user = auth.authenticate(username=new_user_form.cleaned_data['username'],
                                             password=new_user_form.cleaned_data['password2'])

                auth.login(request, new_user)
                return redirect('index')

            else:
                context['form'] = new_user_form

        except(KeyError, ValueError, AttributeError):
            return HttpResponseBadRequest()

    return render_to_response('fantastical_things/registration.html', context)


@login_required(login_url='login')
def all_boards(request):
    boards = Board.objects.filter(users=request.user)

    context = {
        'boards': boards,
    }

    return render(request, 'fantastical_things/boards_list.html', context)


@login_required(login_url='login')
def board(request, board_id):
    board = get_object_or_404(Board, users=request.user, id=board_id)
    # board = Board.objects.filter(users=request.user, id=board_id).first()

    card_lists = board.cardlist_set.filter(users=request.user)
    board_users = board.users.all()

    update_cards(board)

    context = {
        'board': board,
        'board_users': board_users,
        'card_lists': [],
    }

    for card_list in card_lists:

        card_list_dict = {
            'card_list': card_list,
            'cards': []
        }

        cards = card_list.card_set.all().filter(users=request.user)

        for card in cards:
            card_dict = {
                'card': card,
                'tasks': []
            }

            tasks = card.task_set.all().filter(users=request.user)

            card_dict['tasks'] = tasks

            card_list_dict['cards'].append(card_dict)

        context['card_lists'].append(card_list_dict)

    return render(request, 'fantastical_things/board.html', context)


@login_required(login_url='login')
def complete_task(request, board_id, task_id):
    task = get_object_or_404(klass=Task, users=request.user, id=task_id)
    # task = Card.objects.filter(users=request.user, id=task_id).first()

    if task.status is True:
        Task.objects.filter(users=request.user, id=task_id).update(status=False)

    else:
        Task.objects.filter(users=request.user, id=task_id).update(status=True)

    return redirect('board', board_id=board_id)


@login_required(login_url='login')
def edit_board(request, board_id):
    board = get_object_or_404(Board, users=request.user, id=board_id)
    # board = Board.objects.filter(users=request.user, id=board_id).first()

    context = {
        'board': board,
    }

    if request.POST:
        try:
            form = BoardCardlistForm(request.POST)

            if form.is_valid():
                Board.objects.filter(users=request.user, id=board_id).update(
                    title=form.cleaned_data['title'])
                Board.objects.filter(users=request.user, id=board_id).update(
                    description=form.cleaned_data['description'])

            else:
                context['form'] = form
                return render(request, 'fantastical_things/edit/edit_board.html', context)

        except(KeyError, ValueError, AttributeError):
            return HttpResponseBadRequest()

        return redirect('board', board_id=board_id)

    return render(request, 'fantastical_things/edit/edit_board.html', context)


@login_required(login_url='login')
def edit_cardlist(request, board_id, cardlist_id):
    board = get_object_or_404(Board, users=request.user, id=board_id)
    cardlist = get_object_or_404(CardList, users=request.user, id=cardlist_id)
    #
    # board = Board.objects.filter(users=request.user, id=board_id).first()
    # cardlist = Card.objects.filter(users=request.user, id=cardlist_id).first()

    context = {
        'board_id': board.id,
        'cardlist': cardlist,
    }

    if request.POST:
        try:
            form = BoardCardlistForm(request.POST)

            if form.is_valid():
                CardList.objects.filter(users=request.user, id=cardlist_id).update(
                    title=form.cleaned_data['title'])
                CardList.objects.filter(users=request.user, id=cardlist_id).update(
                    description=form.cleaned_data['description'])

            else:
                context['form'] = form
                return render(request, 'fantastical_things/edit/edit_cardlist.html', context)

        except(KeyError, ValueError, AttributeError):
            return HttpResponseBadRequest()

        return redirect('board', board_id=board_id)

    return render(request, 'fantastical_things/edit/edit_cardlist.html', context)


@login_required(login_url='login')
def edit_card(request, board_id, card_id):
    if request.POST:
        try:
            context = {}
            context.update(csrf(request))

            Card.objects.filter(users=request.user, id=card_id).update(title=request.POST['title'])
            Card.objects.filter(users=request.user, id=card_id).update(cardlist=request.POST['moving'])

            deadline = dateutil.parser.parse(request.POST['deadline'] + ' ' + request.POST['deadline_time'])
            if deadline < datetime.datetime.now():
                return HttpResponseBadRequest()

            else:
                Card.objects.filter(users=request.user, id=card_id).update(
                    deadline=deadline + datetime.timedelta(hours=3))

            years = 0
            months = 0
            days = 0
            hours = 0
            minutes = 0
            seconds = 0

            if request.POST['years'] != '':
                years += int(request.POST['years'])
                years = 0 if years < 0 else years

            if request.POST['months'] != '':
                months += int(request.POST['months'])
                months = 0 if months < 0 else months

            if request.POST['days'] != '':
                days += int(request.POST['days'])
                days = 0 if days < 0 else days

            if request.POST['hours'] != '':
                hours += int(request.POST['hours'])
                hours = 0 if hours < 0 else hours

            if request.POST['minutes'] != '':
                minutes += int(request.POST['minutes'])
                minutes = 0 if minutes < 0 else minutes

            if request.POST['seconds'] != '':
                seconds += int(request.POST['seconds'])
                seconds = 0 if seconds < 0 else seconds

            time_delta = relativedelta(years=+years,
                                       months=+months,
                                       days=+days,
                                       hours=+hours,
                                       minutes=+minutes,
                                       seconds=+seconds)

            if years != 0 or months != 0 or days != 0 or hours != 0 or minutes != 0 or seconds != 0:
                Card.objects.filter(users=request.user, id=card_id).update(repeatable=True)

                Card.objects.filter(users=request.user, id=card_id).update(years=years)
                Card.objects.filter(users=request.user, id=card_id).update(years=years)
                Card.objects.filter(users=request.user, id=card_id).update(months=months)
                Card.objects.filter(users=request.user, id=card_id).update(days=days)
                Card.objects.filter(users=request.user, id=card_id).update(hours=hours)
                Card.objects.filter(users=request.user, id=card_id).update(minutes=minutes)
                Card.objects.filter(users=request.user, id=card_id).update(seconds=seconds)

            else:
                Card.objects.filter(users=request.user, id=card_id).update(repeatable=False)

        except(KeyError, ValueError, AttributeError):
            return HttpResponseBadRequest()

        return redirect('board', board_id=board_id)

    card = Card.objects.get(users=request.user, id=card_id)
    board = Board.objects.get(users=request.user, id=board_id)
    cardlists = board.cardlist_set.all()

    context = {
        'board_id': board_id,
        'cardlists': cardlists,
        'card': card,
        'deadline': datetime.datetime.strftime(card.deadline, '%Y-%m-%d'),
        'deadline_time': datetime.datetime.strftime(card.deadline, '%H:%M'),
        # 'now':timezone.datetime.now()
    }

    update_cards(board)

    return render(request, 'fantastical_things/edit/edit_card.html', context)


@login_required(login_url='login')
def edit_task(request, board_id, task_id):
    board = get_object_or_404(Board, users=request.user, id=board_id)
    task = get_object_or_404(Task, users=request.user, id=task_id)
    # board = Board.objects.filter(users=request.user, id=board_id).first()
    # task = Card.objects.filter(users=request.user, id=task_id).first()

    context = {
        'board_id': board_id,
        'task': task,
    }

    if request.POST:
        try:
            form = TaskForm(request.POST)

            if form.is_valid():
                Task.objects.filter(users=request.user, id=task_id).update(
                    title=form.cleaned_data['title'])
                Task.objects.filter(users=request.user, id=task_id).update(
                    description=form.cleaned_data['description'])
                Task.objects.filter(users=request.user, id=task_id).update(status=form.cleaned_data['status'])

            else:
                context['form'] = form
                return render(request, 'fantastical_things/edit/edit_task.html', context)

        except(KeyError, ValueError, AttributeError):
            return HttpResponseBadRequest()

        return redirect('board', board_id=board_id)

    return render(request, 'fantastical_things/edit/edit_task.html', context)


@login_required(login_url='login')
def delete_board(request, board_id):
    try:
        Board.objects.filter(users=request.user, id=board_id).delete()

    except(KeyError, ValueError, AttributeError):
        return HttpResponseBadRequest()
    return redirect('index')


@login_required(login_url='login')
def delete_cardlist(request, board_id, cardlist_id):
    try:
        CardList.objects.filter(users=request.user, id=cardlist_id).delete()

    except(KeyError, ValueError, AttributeError):
        return HttpResponseBadRequest()

    return redirect('board', board_id=board_id)


@login_required(login_url='login')
def delete_card(request, board_id, card_id):
    try:
        Card.objects.filter(users=request.user, id=card_id).delete()

    except(KeyError, ValueError, AttributeError):
        return HttpResponseBadRequest()
    return redirect('board', board_id=board_id)


@login_required(login_url='login')
def delete_task(request, board_id, task_id):
    try:
        Task.objects.filter(users=request.user, id=task_id).delete()

    except(KeyError, ValueError, AttributeError):
        return HttpResponseBadRequest()

    return redirect('board', board_id=board_id)


@login_required(login_url='login')
def add_board(request):
    if request.POST:
        try:
            form = BoardCardlistForm(request.POST)

            if form.is_valid():
                new_board = Board.objects.create(title=form.cleaned_data['title'],
                                                 description=form.cleaned_data['description'],
                                                 user=request.user)
                new_board.users.add(request.user)

                to_do_cardlist = CardList.objects.create(title='To-Do',
                                                         user=request.user)
                doing_cardlist = CardList.objects.create(title='Doing',
                                                         user=request.user)
                done_cardlist = CardList.objects.create(title='Done',
                                                        user=request.user)
                overdue_cardlist = CardList.objects.create(title='Overdue',
                                                           user=request.user)

                new_board.cardlist_set.add(to_do_cardlist)
                new_board.cardlist_set.add(doing_cardlist)
                new_board.cardlist_set.add(done_cardlist)
                new_board.cardlist_set.add(overdue_cardlist)

                to_do_cardlist.users.set(new_board.users.all())
                doing_cardlist.users.set(new_board.users.all())
                done_cardlist.users.set(new_board.users.all())
                overdue_cardlist.users.set(new_board.users.all())

                new_board.save()

            else:
                context = {
                    'form': form
                }
                return render(request, 'fantastical_things/add/add_board.html', context)

        except(KeyError, ValueError, AttributeError):
            return HttpResponseBadRequest()

        return redirect('board', board_id=new_board.id)

    return render(request, 'fantastical_things/add/add_board.html')


@login_required(login_url='login')
def add_cardlist(request, board_id):
    context = {
        'board_id': board_id,
    }

    if request.POST:
        try:
            form = BoardCardlistForm(request.POST)

            if form.is_valid():
                new_cardlist = CardList.objects.create(title=form.cleaned_data['title'],
                                                       description=form.cleaned_data['description'],
                                                       user=request.user)

                # board = get_object_or_404(Board, users=request.user, id=board_id)
                board = Board.objects.filter(users=request.user, id=board_id).first()
                board.cardlist_set.add(new_cardlist)
                new_cardlist.users.set(board.users.all())

                board.save()
                new_cardlist.save()

            else:
                context['form'] = form

                return render(request, 'fantastical_things/add/add_cardlist.html', context)

        except(KeyError, ValueError, AttributeError):
            return HttpResponseBadRequest()

        return redirect('board', board_id=board_id)

    return render(request, 'fantastical_things/add/add_cardlist.html', context)


@login_required(login_url='login')
def add_card(request, board_id, cardlist_id):
    if request.POST:
        # try:
        context = {}
        context.update(csrf(request))
        new_card = Card.objects.create(title=request.POST['title'],
                                       user=request.user,
                                       deadline=None)
        cardlist = CardList.objects.get(users=request.user, id=cardlist_id)
        cardlist.card_set.add(new_card)

        new_card.users.set(cardlist.users.all())

        cardlist.save()
        new_card.save()

        if request.POST['deadline'] != '' and request.POST['deadline_time'] != '':
            deadline = dateutil.parser.parse(request.POST['deadline'] + ' ' + request.POST['deadline_time'])
            if deadline < datetime.datetime.now():
                return HttpResponseBadRequest()

            else:
                new_card.deadline = deadline + datetime.timedelta(hours=3)
                new_card.save()

            years = 0
            months = 0
            days = 0
            hours = 0
            minutes = 0
            seconds = 0

            if request.POST['years'] != '':
                years += int(request.POST['years'])
                years = 0 if years < 0 else years

            if request.POST['months'] != '':
                months += int(request.POST['months'])
                months = 0 if months < 0 else months

            if request.POST['days'] != '':
                days += int(request.POST['days'])
                days = 0 if days < 0 else days

            if request.POST['hours'] != '':
                hours += int(request.POST['hours'])
                hours = 0 if hours < 0 else hours

            if request.POST['minutes'] != '':
                minutes += int(request.POST['minutes'])
                minutes = 0 if minutes < 0 else minutes

            if request.POST['seconds'] != '':
                seconds += int(request.POST['seconds'])
                seconds = 0 if seconds < 0 else seconds

            if years != 0 or months != 0 or days != 0 or hours != 0 or minutes != 0 or seconds != 0:
                new_card.repeatable = True

                new_card.years = years
                new_card.years = years
                new_card.months = months
                new_card.days = days
                new_card.hours = hours
                new_card.minutes = minutes
                new_card.seconds = seconds

            else:
                new_card.repeatable = False

            cardlist = CardList.objects.get(users=request.user, id=cardlist_id)
            cardlist.card_set.add(new_card)

            new_card.users.set(cardlist.users.all())

            cardlist.save()
            new_card.save()
        #
        # except(KeyError, ValueError, AttributeError):
        #     return HttpResponseBadRequest()

        return redirect('board', board_id=board_id)

    context = {
        'board_id': board_id,
        'cardlist_id': cardlist_id
    }

    return render(request, 'fantastical_things/add/add_card.html', context)


@login_required(login_url='login')
def add_task(request, board_id, card_id):
    board = get_object_or_404(Board, users=request.user, id=board_id)
    card = get_object_or_404(Card, users=request.user, id=card_id)
    # board = Board.objects.filter(users=request.user, id=board_id).first()
    # card = Card.objects.filter(users=request.user, id=card_id).first()

    context = {
        'board_id': board_id,
        'card_id': card_id
    }

    if request.POST:
        try:
            form = TaskForm(request.POST)

            if form.is_valid():
                new_task = Task.objects.create(title=form.cleaned_data['title'],
                                               description=form.cleaned_data['description'],
                                               status=form.cleaned_data['status'],
                                               user=request.user)

                card.task_set.add(new_task)
                new_task.users.set(card.users.all())

                card.save()
                new_task.save()

            else:
                context['form'] = form

                return render(request, 'fantastical_things/add/add_task.html', context)

        except(KeyError, ValueError, AttributeError):
            return HttpResponseBadRequest()

        return redirect('board', board_id=board_id)

    return render(request, 'fantastical_things/add/add_task.html', context)


@login_required(login_url='login')
def add_user_to_board(request, board_id):
    board = get_object_or_404(Board, users=request.user, id=board_id)

    context = {
        'board': board,
    }

    if request.POST:
        try:
            context = {}
            context.update(csrf(request))

            user_login = request.POST['user_login']
            new_user = User.objects.filter(username=user_login).first()

            if new_user is not None:
                board.users.add(new_user)
                add_user_to_all_tasks(board, new_user)

                board.users.add(new_user)
                add_user_to_all_tasks(board, new_user)

                board.save()

            else:
                context = {'error': "User doesn't exist",
                           'board': board}

                return render(request, 'fantastical_things/edit/edit_board.html', context)

        except(KeyError, ValueError, AttributeError):
            return HttpResponseBadRequest()

        return redirect('board', board_id=board.id)

    return render(request, 'fantastical_things/edit/edit_board.html', context)


@login_required(login_url='login')
def quit_from_board(request, board_id):
    try:
        if request.POST:
            board = get_object_or_404(klass=Board, users=request.user, id=board_id)

            board.users.remove(request.user)
            board.save()

        return redirect('/')

    except(KeyError, ValueError, AttributeError):
        return HttpResponseBadRequest()
