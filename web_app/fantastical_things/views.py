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
    # card = Card.objects.filter(users=request.user, id=card_id).first()
    # board = Board.objects.filter(users=request.user, id=board_id).first()
    card = get_object_or_404(klass=Card, users=request.user, id=card_id)
    board = get_object_or_404(klass=Board, users=request.user, id=board_id)
    cardlists = board.cardlist_set.all()

    context = {
        'board_id': board.id,
        'card': card,
        'cardlists': cardlists
    }

    if card.deadline is not None:
        context['deadline'] = datetime.datetime.strftime(card.deadline, '%Y-%m-%d')
        context['deadline_time'] = datetime.datetime.strftime(card.deadline, '%H:%M')

    if request.POST:
        try:
            form = CardForm(request.POST)

            if form.is_valid():
                Card.objects.filter(users=request.user, id=card_id).update(title=form.cleaned_data['title'])
                cardlist = get_object_or_404(klass=CardList, id=form.cleaned_data['moving'])
                Card.objects.filter(users=request.user, id=card_id).update(cardlist=form.cleaned_data['moving'])

                deadline_date = form.cleaned_data['deadline']
                deadline_time = form.cleaned_data['deadline_time']

                if deadline_date is not None and deadline_time is not None:
                    deadline = dateutil.parser.parse(timestr=(str(deadline_date) + " " + str(deadline_time)))
                    if deadline < datetime.datetime.now() + datetime.timedelta(hours=3):
                        context['error'] = 'Input correct date or time'
                        return render(request, 'fantastical_things/edit/edit_card.html', context)

                    else:
                        Card.objects.filter(users=request.user, id=card_id).update(
                            deadline=deadline)

                years = form.cleaned_data['years']
                months = form.cleaned_data['months']
                days = form.cleaned_data['days']
                hours = form.cleaned_data['hours']
                minutes = form.cleaned_data['minutes']
                seconds = form.cleaned_data['seconds']

                if years != 0 or months != 0 or days != 0 or hours != 0 or minutes != 0 or seconds != 0:
                    card.repeatable = True

                    card.years = years
                    card.months = months
                    card.days = days
                    card.hours = hours
                    card.minutes = minutes
                    card.seconds = seconds

                    card.save()

                else:
                    Card.objects.filter(users=request.user, id=card_id).update(repeatable=False)

                return redirect('board', board_id=board.id)

            else:
                context['form'] = form
                return render(request, 'fantastical_things/edit/edit_card.html', context)

        except(KeyError, ValueError, AttributeError):
            return HttpResponseBadRequest()

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
    context = {
        'board_id': board_id,
        'cardlist_id': cardlist_id
    }

    if request.POST:
        # try:
        form = CardForm(request.POST)

        if form.is_valid():

            new_card = Card.objects.create(title=form.cleaned_data['title'],
                                           user=request.user,
                                           deadline=None)

            cardlist = get_object_or_404(klass=CardList, id=cardlist_id)
            cardlist.card_set.add(new_card)
            new_card.users.set(cardlist.users.all())

            cardlist.save()
            new_card.save()

            deadline_date = form.cleaned_data['deadline']
            deadline_time = form.cleaned_data['deadline_time']

            if deadline_date is not None and deadline_time is not None:
                deadline = dateutil.parser.parse(timestr=(str(deadline_date) + " " + str(deadline_time)))

                if deadline < datetime.datetime.now() + datetime.timedelta(hours=3):
                    context['error'] = 'Input correct date or time'
                    return render(request, 'fantastical_things/add/add_card.html', context)

                else:
                    Card.objects.filter(users=request.user, id=new_card.id).update(
                        deadline=deadline)

            new_card.years = form.cleaned_data['years'] if form.cleaned_data['years'] is not None else 0
            new_card.months = form.cleaned_data['months'] if form.cleaned_data['months'] is not None else 0
            new_card.days = form.cleaned_data['days'] if form.cleaned_data['days'] is not None else 0
            new_card.hours = form.cleaned_data['hours'] if form.cleaned_data['hours'] is not None else 0
            new_card.minutes = form.cleaned_data['minutes'] if form.cleaned_data['minutes'] is not None else 0
            new_card.seconds = form.cleaned_data['seconds'] if form.cleaned_data['seconds'] is not None else 0

            if new_card.years != 0 or new_card.months != 0 or new_card.days != 0 or \
                    new_card.hours != 0 or new_card.minutes != 0 or new_card.seconds != 0:
                new_card.repeatable = True

            new_card.save()

            cardlist = CardList.objects.get(users=request.user, id=cardlist_id)
            cardlist.card_set.add(new_card)

            new_card.users.set(cardlist.users.all())

            cardlist.save()
            new_card.save()

            return redirect('board', board_id=board_id)
        else:
            context['form'] = form

            return render(request, 'fantastical_things/add/add_card.html', context)
    #
    # except(KeyError, ValueError, AttributeError):
    #     return HttpResponseBadRequest()
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
