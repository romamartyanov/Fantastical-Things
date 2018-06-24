from django.shortcuts import render_to_response, redirect, render
from django.template.context_processors import csrf
from django.contrib import auth

from .user_creation_form import UserCreateForm
from .models import *


def login(request):
    context = {}
    context.update(csrf(request))

    if request.POST:
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')

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
        new_user_form = UserCreateForm(request.POST)

        if new_user_form.is_valid():
            new_user_form.save()
            new_user = auth.authenticate(username=new_user_form.cleaned_data['username'],
                                         password=new_user_form.cleaned_data['password2'])

            auth.login(request, new_user)
            return redirect('/')

        else:
            context['form'] = new_user_form

    return render_to_response('fantastical_things/registration.html', context)


def index(request):
    if not request.user.is_authenticated:
        return redirect('/login/')

    return render(request, 'fantastical_things/index.html')


def all_boards(request):
    if not request.user.is_authenticated:
        return redirect('/login/')

    # username = auth.get_user(request).username

    boards = Board.objects.filter(user=request.user)

    context = {
        'boards': boards,
    }

    return render(request, 'fantastical_things/boards_list.html', context)


def board(request, board_id):
    if not request.user.is_authenticated:
        return redirect('/login/')

    # username = auth.get_user(request).username

    board = Board.objects.get(user=request.user, id=board_id)
    card_lists = board.cardlist_set.all().filter(user=request.user)

    context = {
        'board': board,
        'card_lists': [],
    }

    for card_list in card_lists:

        card_list_dict = {
            'card_list': card_list,
            'cards': []
        }

        cards = card_list.card_set.all().filter(user=request.user)

        for card in cards:
            card_dict = {
                'card': card,
                'tasks': []
            }

            tasks = card.task_set.all().filter(user=request.user)

            card_dict['tasks'] = tasks

            card_list_dict['cards'].append(card_dict)

        context['card_lists'].append(card_list_dict)

    return render(request, 'fantastical_things/board.html', context)


def complete_task(request, board_id, task_id):
    if not request.user.is_authenticated:
        return redirect('/login/')

    task = Task.objects.get(user=request.user, id=task_id)

    if task.status is True:
        Task.objects.filter(user=request.user, id=task_id).update(status=False)

    else:
        Task.objects.filter(user=request.user, id=task_id).update(status=True)

    return redirect('/board/' + board_id)


def edit_board(request, board_id):
    if not request.user.is_authenticated:
        return redirect('/login/')

    if request.POST:
        context = {}
        context.update(csrf(request))

        Board.objects.filter(user=request.user, id=board_id).update(title=request.POST['title'])
        Board.objects.filter(user=request.user, id=board_id).update(description=request.POST['description'])

        # добавить проверку
        return redirect('/board/' + board_id)

    board = Board.objects.get(user=request.user, id=board_id)

    context = {
        'board': board,
    }

    return render(request, 'fantastical_things/edit/edit_board.html', context)


def edit_cardlist(request, board_id, cardlist_id):
    if not request.user.is_authenticated:
        return redirect('/login/')

    if request.POST:
        context = {}
        context.update(csrf(request))

        CardList.objects.filter(user=request.user, id=cardlist_id).update(title=request.POST['title'])
        CardList.objects.filter(user=request.user, id=cardlist_id).update(description=request.POST['description'])

        # добавить проверку
        return redirect('/board/' + board_id)

    cardlist = CardList.objects.get(user=request.user, id=cardlist_id)

    context = {
        'board_id': board_id,
        'cardlist': cardlist,
    }

    return render(request, 'fantastical_things/edit/edit_cardlist.html', context)


def edit_card(request, board_id, card_id):
    if not request.user.is_authenticated:
        return redirect('/login/')

    if request.POST:
        context = {}
        context.update(csrf(request))

        Card.objects.filter(user=request.user, id=card_id).update(title=request.POST['title'])
        Card.objects.filter(user=request.user, id=card_id).update(cardlist=request.POST['moving'])

        # добавить проверку
        return redirect('/board/' + board_id)

    card = Card.objects.get(user=request.user, id=card_id)
    board = Board.objects.get(user=request.user, id=board_id)
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
        context = {}
        context.update(csrf(request))

        Task.objects.filter(user=request.user, id=task_id).update(title=request.POST['title'])
        Task.objects.filter(user=request.user, id=task_id).update(description=request.POST['description'])
        Task.objects.filter(user=request.user, id=task_id).update(status=request.POST['status'])

        # добавить проверку
        return redirect('/board/' + board_id)

    task = Task.objects.get(user=request.user, id=task_id)

    context = {
        'board_id': board_id,
        'task': task,
    }

    return render(request, 'fantastical_things/edit/edit_task.html', context)


def delete_board(request, board_id):
    if not request.user.is_authenticated:
        return redirect('/login/')

    Board.objects.filter(user=request.user, id=board_id).delete()

    return redirect('/')


def delete_cardlist(request, board_id, cardlist_id):
    if not request.user.is_authenticated:
        return redirect('/login/')

    CardList.objects.filter(user=request.user, id=cardlist_id).delete()

    return redirect('/board/' + board_id)


def delete_card(request, board_id, card_id):
    if not request.user.is_authenticated:
        return redirect('/login/')

    Card.objects.filter(user=request.user, id=card_id).delete()

    return redirect('/board/' + board_id)


def delete_task(request, board_id, task_id):
    if not request.user.is_authenticated:
        return redirect('/login/')

    Task.objects.filter(user=request.user, id=task_id).delete()

    return redirect('/board/' + board_id)


def add_board(request):
    if not request.user.is_authenticated:
        return redirect('/login/')

    if request.POST:
        context = {}
        context.update(csrf(request))
        new_board = Board.objects.create(title=request.POST['title'],
                                         description=request.POST['description'],
                                         user=request.user)

        new_board.save()

        # добавить проверку
        return redirect('/')

    return render(request, 'fantastical_things/add/add_board.html')


def add_cardlist(request, board_id):
    if not request.user.is_authenticated:
        return redirect('/login/')

    if request.POST:
        context = {}
        context.update(csrf(request))
        new_cardlist = CardList.objects.create(title=request.POST['title'],
                                               description=request.POST['description'],
                                               user=request.user)

        board = Board.objects.get(user=request.user, id=board_id)
        board.cardlist_set.add(new_cardlist)
        board.save()
        new_cardlist.save()

        # добавить проверку
        return redirect('/board/' + board_id)

    context = {
        'board_id': board_id,
    }

    return render(request, 'fantastical_things/add/add_cardlist.html', context)


def add_card(request, board_id, cardlist_id):
    if not request.user.is_authenticated:
        return redirect('/login/')

    if request.POST:
        context = {}
        context.update(csrf(request))
        new_card = Card.objects.create(title=request.POST['title'],
                                       user=request.user)

        cardlist = CardList.objects.get(user=request.user, id=cardlist_id)
        cardlist.card_set.add(new_card)
        cardlist.save()
        new_card.save()

        # добавить проверку
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
        context = {}
        context.update(csrf(request))
        new_task = Task.objects.create(title=request.POST['title'],
                                       description=request.POST['description'],
                                       status=False,
                                       user=request.user)

        card = Card.objects.get(user=request.user, id=card_id)
        card.task_set.add(new_task)
        card.save()
        new_task.save()

        # добавить проверку
        return redirect('/board/' + board_id)

    context = {
        'board_id': board_id,
        'card_id': card_id
    }

    return render(request, 'fantastical_things/add/add_task.html', context)
