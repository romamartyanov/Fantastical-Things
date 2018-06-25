from django.shortcuts import render_to_response, redirect, render
from django.template.context_processors import csrf
from django.contrib import auth
from django.http.response import HttpResponseBadRequest

from .forms import UserCreateForm
from .models import *
from django.contrib.auth.models import User

import datetime
from dateutil.relativedelta import *


def update_cards(board):
    card_lists = board.cardlist_set.all()

    try:
        overdue_cardlist = board.cardlist_set.get(title='Overdue')
        to_do = board.cardlist_set.get(title='To-Do')
    except CardList.DoesNotExist:

        return

    for card_list in card_lists:
        cards = card_list.card_set.all()

        for card in cards:

            deadline = datetime.datetime.strptime(card.deadline, '%Y-%m-%d')

            if deadline < datetime.datetime.now():
                if card.repeatable:
                    time_delta = relativedelta(years=+card.years,
                                               months=+card.months,
                                               days=+card.days,
                                               hours=+card.hours,
                                               minutes=+card.minutes,
                                               seconds=+card.seconds)

                    new_deadline = deadline + time_delta

                    card.deadline = new_deadline
                    Card.objects.filter(id=card.id).update(cardlist=to_do)
                    card.save()

                elif not card.repeatable:
                    Card.objects.filter(id=card.id).update(cardlist=overdue_cardlist)
                    card.save()


def login(request):
    context = {}
    context.update(csrf(request))

    if request.POST:
        try:
            username = request.POST.get('username', '')
            password = request.POST.get('password', '')

        except(KeyError, ValueError, AttributeError):
            return HttpResponseBadRequest()

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('/')

        else:
            context['login_error'] = "Wrong"
            return render_to_response('fantastical_things/login.html', context)

    return render_to_response('fantastical_things/login.html', context)


def logout(request):
    auth.logout(request)
    return redirect('/login/')


def registration(request):
    context = {}
    context.update(csrf(request))
    context['form'] = UserCreateForm()

    if request.POST:
        try:
            new_user_form = UserCreateForm(request.POST)

            if new_user_form.is_valid():
                new_user_form.save()
                new_user = auth.authenticate(username=new_user_form.cleaned_data['username'],
                                             password=new_user_form.cleaned_data['password2'])

                auth.login(request, new_user)
                return redirect('/')

            else:
                context['form'] = new_user_form

        except(KeyError, ValueError, AttributeError):
            return HttpResponseBadRequest()

    return render_to_response('fantastical_things/registration.html', context)


def index(request):
    if not request.user.is_authenticated:
        return redirect('/login/')

    return render(request, 'fantastical_things/index.html')


def all_boards(request):
    if not request.user.is_authenticated:
        return redirect('/login/')

    # username = auth.get_user(request).username

    boards = Board.objects.filter(users=request.user)

    context = {
        'boards': boards,
    }

    return render(request, 'fantastical_things/boards_list.html', context)


def board(request, board_id):
    if not request.user.is_authenticated:
        return redirect('/login/')

    # username = auth.get_user(request).username

    board = Board.objects.get(users=request.user, id=board_id)
    card_lists = board.cardlist_set.filter(users=request.user)
    board_users = board.users.all()

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


def complete_task(request, board_id, task_id):
    if not request.user.is_authenticated:
        return redirect('/login/')

    task = Task.objects.get(users=request.user, id=task_id)

    if task.status is True:
        Task.objects.filter(users=request.user, id=task_id).update(status=False)

    else:
        Task.objects.filter(users=request.user, id=task_id).update(status=True)

    return redirect('/board/' + board_id)


def edit_board(request, board_id):
    if not request.user.is_authenticated:
        return redirect('/login/')

    if request.POST:
        try:
            context = {}
            context.update(csrf(request))

            Board.objects.filter(users=request.user, id=board_id).update(title=request.POST['title'])
            Board.objects.filter(users=request.user, id=board_id).update(description=request.POST['description'])

        except(KeyError, ValueError, AttributeError):
            return HttpResponseBadRequest()

        return redirect('/board/' + board_id)

    board = Board.objects.get(users=request.user, id=board_id)

    context = {
        'board': board,
    }

    return render(request, 'fantastical_things/edit/edit_board.html', context)


def edit_cardlist(request, board_id, cardlist_id):
    if not request.user.is_authenticated:
        return redirect('/login/')

    if request.POST:
        try:
            context = {}
            context.update(csrf(request))

            CardList.objects.filter(users=request.user, id=cardlist_id).update(title=request.POST['title'])
            CardList.objects.filter(users=request.user, id=cardlist_id).update(description=request.POST['description'])

        except(KeyError, ValueError, AttributeError):
            return HttpResponseBadRequest()

        return redirect('/board/' + board_id)

    cardlist = CardList.objects.get(users=request.user, id=cardlist_id)

    context = {
        'board_id': board_id,
        'cardlist': cardlist,
    }

    return render(request, 'fantastical_things/edit/edit_cardlist.html', context)


def edit_card(request, board_id, card_id):
    if not request.user.is_authenticated:
        return redirect('/login/')

    if request.POST:
        try:
            context = {}
            context.update(csrf(request))

            Card.objects.filter(users=request.user, id=card_id).update(title=request.POST['title'])
            Card.objects.filter(users=request.user, id=card_id).update(cardlist=request.POST['moving'])

            # deadline = datetime.datetime.strptime(request.POST['deadline'], '%Y-%m-%d')
            # if deadline < datetime.datetime.now():
            #     return HttpResponseBadRequest()
            #
            # else:
            #     Card.objects.filter(users=request.user, id=card_id).update(cardlist=request.POST['deadline'])
            #
            # years = 0
            # months = 0
            # days = 0
            # hours = 0
            # minutes = 0
            # seconds = 0
            #
            # if request.POST['years'] != '':
            #     years += int(request.POST['years'])
            #     years = 0 if years < 0 else years
            #
            # if request.POST['months'] != '':
            #     months += int(request.POST['months'])
            #     months = 0 if months < 0 else months
            #
            # if request.POST['days'] != '':
            #     days += int(request.POST['days'])
            #     days = 0 if days < 0 else days
            #
            # if request.POST['hours'] != '':
            #     hours += int(request.POST['hours'])
            #     hours = 0 if hours < 0 else hours
            #
            # if request.POST['minutes'] != '':
            #     minutes += int(request.POST['minutes'])
            #     minutes = 0 if minutes < 0 else minutes
            #
            # if request.POST['seconds'] != '':
            #     seconds += int(request.POST['seconds'])
            #     seconds = 0 if seconds < 0 else seconds
            #
            # time_delta = relativedelta(years=+years,
            #                            months=+months,
            #                            days=+days,
            #                            hours=+hours,
            #                            minutes=+minutes,
            #                            seconds=+seconds)
            #
            # if years != 0 or months != 0 or days != 0 or hours != 0 or minutes != 0 or seconds != 0:
            #     Card.objects.filter(users=request.user, id=card_id).update(repeatable=True)
            #
            #     Card.objects.filter(users=request.user, id=card_id).update(years=years)
            #     Card.objects.filter(users=request.user, id=card_id).update(years=years)
            #     Card.objects.filter(users=request.user, id=card_id).update(months=months)
            #     Card.objects.filter(users=request.user, id=card_id).update(days=days)
            #     Card.objects.filter(users=request.user, id=card_id).update(hours=hours)
            #     Card.objects.filter(users=request.user, id=card_id).update(minutes=minutes)
            #     Card.objects.filter(users=request.user, id=card_id).update(seconds=seconds)
            #
            # else:
            #     Card.objects.filter(users=request.user, id=card_id).update(repeatable=False)

        except(KeyError, ValueError, AttributeError):
            return HttpResponseBadRequest()

        return redirect('/board/' + board_id)

    card = Card.objects.get(users=request.user, id=card_id)
    board = Board.objects.get(users=request.user, id=board_id)
    cardlists = board.cardlist_set.all()

    context = {
        'board_id': board_id,
        'cardlists': cardlists,
        'card': card,
    }

    return render(request, 'fantastical_things/edit/edit_card.html', context)


def edit_task(request, board_id, task_id):
    if not request.user.is_authenticated:
        return redirect('/login/')

    if request.POST:
        try:
            context = {}
            context.update(csrf(request))

            Task.objects.filter(users=request.user, id=task_id).update(title=request.POST['title'])
            Task.objects.filter(users=request.user, id=task_id).update(description=request.POST['description'])
            Task.objects.filter(users=request.user, id=task_id).update(status=request.POST['status'])

        except(KeyError, ValueError, AttributeError):
            return HttpResponseBadRequest()

        return redirect('/board/' + board_id)

    # task = Task.objects.get(user=request.user, id=task_id)
    task = Task.objects.get(id=task_id)

    context = {
        'board_id': board_id,
        'task': task,
    }

    return render(request, 'fantastical_things/edit/edit_task.html', context)


def delete_board(request, board_id):
    if not request.user.is_authenticated:
        return redirect('/login/')

    try:
        Board.objects.filter(users=request.user, id=board_id).delete()

    except(KeyError, ValueError, AttributeError):
        return HttpResponseBadRequest()
    return redirect('/')


def delete_cardlist(request, board_id, cardlist_id):
    if not request.user.is_authenticated:
        return redirect('/login/')

    try:
        CardList.objects.filter(users=request.user, id=cardlist_id).delete()

    except(KeyError, ValueError, AttributeError):
        return HttpResponseBadRequest()

    return redirect('/board/' + board_id)


def delete_card(request, board_id, card_id):
    if not request.user.is_authenticated:
        return redirect('/login/')

    try:
        Card.objects.filter(users=request.user, id=card_id).delete()

    except(KeyError, ValueError, AttributeError):
        return HttpResponseBadRequest()
    return redirect('/board/' + board_id)


def delete_task(request, board_id, task_id):
    if not request.user.is_authenticated:
        return redirect('/login/')

    try:
        Task.objects.filter(users=request.user, id=task_id).delete()

    except(KeyError, ValueError, AttributeError):
        return HttpResponseBadRequest()

    return redirect('/board/' + board_id)


def add_board(request):
    if not request.user.is_authenticated:
        return redirect('/login/')

    if request.POST:
        try:
            context = {}
            context.update(csrf(request))
            new_board = Board.objects.create(title=request.POST['title'],
                                             description=request.POST['description'],
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

        except(KeyError, ValueError, AttributeError):
            return HttpResponseBadRequest()

        return redirect('/')

    return render(request, 'fantastical_things/add/add_board.html')


def add_cardlist(request, board_id):
    if not request.user.is_authenticated:
        return redirect('/login/')

    if request.POST:
        try:
            context = {}
            context.update(csrf(request))
            new_cardlist = CardList.objects.create(title=request.POST['title'],
                                                   description=request.POST['description'],
                                                   user=request.user)

            board = Board.objects.get(users=request.user, id=board_id)
            board.cardlist_set.add(new_cardlist)

            new_cardlist.users.set(board.users.all())

            board.save()
            new_cardlist.save()

        except(KeyError, ValueError, AttributeError):
            return HttpResponseBadRequest()

        return redirect('/board/' + board_id)

    context = {
        'board_id': board_id,
    }

    return render(request, 'fantastical_things/add/add_cardlist.html', context)


def add_card(request, board_id, cardlist_id):
    if not request.user.is_authenticated:
        return redirect('/login/')

    if request.POST:
        try:
            context = {}
            context.update(csrf(request))
            new_card = Card.objects.create(title=request.POST['title'],
                                           user=request.user)

            # deadline = datetime.datetime.strptime(request.POST['deadline'], '%Y-%m-%d')
            # if deadline < datetime.datetime.now():
            #     return HttpResponseBadRequest()
            #
            # else:
            #     new_card.deadline = request.POST['deadline']
            #
            # years = 0
            # months = 0
            # days = 0
            # hours = 0
            # minutes = 0
            # seconds = 0
            #
            # if request.POST['years'] != '':
            #     years += int(request.POST['years'])
            #     years = 0 if years < 0 else years
            #
            # if request.POST['months'] != '':
            #     months += int(request.POST['months'])
            #     months = 0 if months < 0 else months
            #
            # if request.POST['days'] != '':
            #     days += int(request.POST['days'])
            #     days = 0 if days < 0 else days
            #
            # if request.POST['hours'] != '':
            #     hours += int(request.POST['hours'])
            #     hours = 0 if hours < 0 else hours
            #
            # if request.POST['minutes'] != '':
            #     minutes += int(request.POST['minutes'])
            #     minutes = 0 if minutes < 0 else minutes
            #
            # if request.POST['seconds'] != '':
            #     seconds += int(request.POST['seconds'])
            #     seconds = 0 if seconds < 0 else seconds
            #
            # if years != 0 or months != 0 or days != 0 or hours != 0 or minutes != 0 or seconds != 0:
            #     new_card.repeatable = True
            #
            #     new_card.years = years
            #     new_card.years = years
            #     new_card.months = months
            #     new_card.days = days
            #     new_card.hours = hours
            #     new_card.minutes = minutes
            #     new_card.seconds = seconds
            #
            # else:
            #     new_card.repeatable = False
            #
            cardlist = CardList.objects.get(users=request.user, id=cardlist_id)
            cardlist.card_set.add(new_card)

            new_card.users.set(cardlist.users.all())

            cardlist.save()
            new_card.save()

        except(KeyError, ValueError, AttributeError):
            return HttpResponseBadRequest()

        return redirect('/board/' + board_id)

    context = {
        'board_id': board_id,
        'cardlist_id': cardlist_id
    }

    return render(request, 'fantastical_things/add/add_card.html', context)


def add_task(request, board_id, card_id):
    if not request.user.is_authenticated:
        return redirect('/login/')

    if request.POST:
        try:
            context = {}
            context.update(csrf(request))
            new_task = Task.objects.create(title=request.POST['title'],
                                           description=request.POST['description'],
                                           status=False,
                                           user=request.user)

            card = Card.objects.get(users=request.user, id=card_id)
            card.task_set.add(new_task)

            new_task.users.set(card.users.all())

            card.save()
            new_task.save()

        except(KeyError, ValueError, AttributeError):
            return HttpResponseBadRequest()

        return redirect('/board/' + board_id)

    context = {
        'board_id': board_id,
        'card_id': card_id
    }

    return render(request, 'fantastical_things/add/add_task.html', context)


def add_user_to_all_tasks(board, new_user):
    card_lists = board.cardlist_set.all()

    for card_list in card_lists:
        cards = card_list.card_set.all()

        for card in cards:
            tasks = card.task_set.all()

            for task in tasks:
                task.users.add(new_user)
                task.save()

            card.users.add(new_user)
            card.save()

        card_list.users.add(new_user)
        card_list.save()


def add_user_to_board(request, board_id):
    if not request.user.is_authenticated:
        return redirect('/login/')

    if request.POST:
        try:
            context = {}
            context.update(csrf(request))

            new_user = User.objects.get(username=request.POST['user_login'])

            board = Board.objects.get(users=request.user, id=board_id)
            # empty_board = Board.objects.filter(users=new_user, id=board_id)

            board.users.add(new_user)
            add_user_to_all_tasks(board, new_user)

            board.save()

        except(KeyError, ValueError, AttributeError):
            return HttpResponseBadRequest()

        return redirect('/board/' + board_id)

    board = Board.objects.get(users=request.user, id=board_id)

    context = {
        'board': board,
    }

    return render(request, 'fantastical_things/edit/edit_board.html', context)


def quit_from_board(request, board_id):
    if not request.user.is_authenticated:
        return redirect('/login/')

    try:
        context = {}
        context.update(csrf(request))

        board = Board.objects.get(users=request.user, id=board_id)

        board.users.remove(request.user)
        board.save()

    except(KeyError, ValueError, AttributeError):
        return HttpResponseBadRequest()

    return redirect('/')
