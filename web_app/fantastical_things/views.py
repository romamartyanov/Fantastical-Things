from django.shortcuts import render

from django.http import *
from django.shortcuts import render_to_response, redirect
from django.template.context_processors import csrf
from django.contrib import auth

from .user_creation_form import UserCreateForm


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


def profile(request):
    pass