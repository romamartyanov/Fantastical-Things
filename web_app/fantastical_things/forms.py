from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django import forms


class UserCreateForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(UserCreateForm, self).__init__(*args, **kwargs)


class UserAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(AuthenticationForm, self).__init__(*args, **kwargs)


class BoardCardlistForm(forms.Form):
    title = forms.CharField(max_length=40, required=True)
    description = forms.CharField(max_length=100, widget=forms.Textarea, required=False)


class TaskForm(forms.Form):
    title = forms.CharField(max_length=40)
    description = forms.CharField(max_length=100, widget=forms.Textarea, required=False)
    status = forms.BooleanField(initial=True, required=False)


class CardForm(forms.Form):
    title = forms.CharField(max_length=40)

    moving = forms.IntegerField(initial=True, required=False)

    deadline = forms.DateField(initial=True, required=False)
    deadline_time = forms.TimeField(initial=True, required=False)

    years = forms.IntegerField(min_value=0, initial=True, required=False)
    months = forms.IntegerField(min_value=0, initial=True, required=False)
    days = forms.IntegerField(min_value=0, initial=True, required=False)
    hours = forms.IntegerField(min_value=0, initial=True, required=False)
    minutes = forms.IntegerField(min_value=0, initial=True, required=False)
    seconds = forms.IntegerField(min_value=0, initial=True, required=False)
