from django.shortcuts import render


def index(request):
    return render(request, 'fantastical_things/index.html')
