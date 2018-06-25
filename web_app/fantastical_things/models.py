from django.db import models
from django.contrib.auth.models import User

from datetime import datetime


class Board(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None, null=True)
    users = models.ManyToManyField(User, related_name='board_users', default=None, null=True, blank=True)

    title = models.CharField(max_length=100)
    description = models.TextField(max_length=100)

    begin_time = models.DateTimeField(default=datetime.now)


class CardList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None, null=True)
    users = models.ManyToManyField(User, related_name='cardlist_users', default=None, null=True, blank=True)

    title = models.CharField(max_length=100)
    description = models.TextField(max_length=100)

    begin_time = models.DateTimeField(default=datetime.now)

    board = models.ForeignKey(Board, on_delete=models.CASCADE, default=None, blank=True, null=True)


class Card(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None, null=True)
    users = models.ManyToManyField(User, related_name='card_users', default=None, null=True, blank=True)

    title = models.CharField(max_length=100)

    begin_time = models.DateTimeField(default=datetime.now)
    deadline = models.DateTimeField(default=datetime.now)

    repeatable = models.BooleanField(default=False)
    years = models.CharField(max_length=10000)
    month = models.CharField(max_length=10000)
    days = models.CharField(max_length=10000)
    hours = models.CharField(max_length=10000)
    minutes = models.CharField(max_length=10000)
    seconds = models.CharField(max_length=10000)

    cardlist = models.ForeignKey(CardList, on_delete=models.CASCADE, default=None, blank=True, null=True)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='children', on_delete=models.CASCADE, )


class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None, null=True)
    users = models.ManyToManyField(User, related_name='task_users', default=None, null=True, blank=True)

    title = models.CharField(max_length=100)
    description = models.TextField(max_length=100)

    status = models.BooleanField(default=False)

    begin_time = models.DateTimeField(default=datetime.now)
    # deadline = models.DateTimeField(default=None, blank=True, null=True)
    # repeatable_time = models.DateTimeField(default=None, blank=True, null=True)

    card = models.ForeignKey(Card, on_delete=models.CASCADE, default=None, blank=True, null=True)

    # parent = models.ForeignKey('self', null=True, blank=True, related_name='children', on_delete=models.CASCADE, )

    def __str__(self):
        return self.title
