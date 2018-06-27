from django.contrib import admin
from .models import Task, Card, CardList, Board

admin.site.register(Task)
admin.site.register(Card)
admin.site.register(CardList)
admin.site.register(Board)


