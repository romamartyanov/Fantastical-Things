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

    username = auth.get_user(request).username
    boards = Board.objects.filter(user=request.user)

    context = {
        'boards': boards,
    }

    return render(request, 'fantastical_things/boards_list.html', context)


# def create_view_board_context(request, board_id):
#     board = Board.objects.get(user=request.user, id=board_id)
#     card_lists = board.cardlist_set.all().filter(user=request.user)
#
#     context = {
#         'board': board,
#         'card_lists': [],
#     }
#
#     for card_list in card_lists:
#
#         card_list_dict = {
#             'card_list': card_list,
#             'cards': []
#         }
#
#         cards = card_list.card_set.all().filter(user=request.user)
#
#         for card in cards:
#             card_dict = {
#                 'card': card,
#                 'tasks': []
#             }
#
#             tasks = card.task_set.all().filter(user=request.user)
#
#             card_dict['tasks'] = tasks
#
#             card_list_dict['cards'].append(card_dict)
#
#         context['card_lists'].append(card_list_dict)
#
#     return context


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

    # context = create_view_board_context(request, board_id)

    return render(request, 'fantastical_things/board.html', context)


def complete_task(request, board_id, task_id):
    if not request.user.is_authenticated:
        return redirect('/login/')

    task = Task.objects.get(user=request.user, id=task_id)

    if task.status is True:
        Task.objects.filter(user=request.user, id=task_id).update(status=False)

    else:
        Task.objects.filter(user=request.user, id=task_id).update(status=True)

    return redirect('/board/'+board_id)

