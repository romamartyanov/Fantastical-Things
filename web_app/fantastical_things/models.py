from django.db import models
from django.contrib.auth.models import User

from datetime import datetime


class Board(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None, null=True)
    users = models.ManyToManyField(User, related_name='board_users', default=None, null=True, blank=True)

    title = models.CharField(max_length=40)
    description = models.TextField(max_length=100)

    begin_time = models.DateTimeField(default=datetime.now)


class CardList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None, null=True)
    users = models.ManyToManyField(User, related_name='cardlist_users', default=None, null=True, blank=True)

    title = models.CharField(max_length=40)
    description = models.TextField(max_length=100)

    begin_time = models.DateTimeField(default=datetime.now)

    board = models.ForeignKey(Board, on_delete=models.CASCADE, default=None, blank=True, null=True)


class Card(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None, null=True)
    users = models.ManyToManyField(User, related_name='card_users', default=None, null=True, blank=True)

    title = models.CharField(max_length=40)

    begin_time = models.DateTimeField(default=datetime.now)
    deadline = models.DateTimeField(default=None, null=True, blank=True)

    repeatable = models.BooleanField(default=False)
    years = models.SmallIntegerField(default=None, blank=True, null=True)
    months = models.SmallIntegerField(default=None, blank=True, null=True)
    days = models.SmallIntegerField(default=None, blank=True, null=True)
    hours = models.SmallIntegerField(default=None, blank=True, null=True)
    minutes = models.SmallIntegerField(default=None, blank=True, null=True)
    seconds = models.SmallIntegerField(default=None, blank=True, null=True)

    cardlist = models.ForeignKey(CardList, on_delete=models.CASCADE, default=None, blank=True, null=True)


class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None, null=True)
    users = models.ManyToManyField(User, related_name='task_users', default=None, null=True, blank=True)

    title = models.CharField(max_length=40)
    description = models.TextField(max_length=100)
    status = models.BooleanField(default=False)

    begin_time = models.DateTimeField(default=datetime.now)
    card = models.ForeignKey(Card, on_delete=models.CASCADE, default=None, blank=True, null=True)

    def __str__(self):
        return self.title
