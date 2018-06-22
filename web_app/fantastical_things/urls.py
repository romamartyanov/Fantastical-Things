from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^login/?$', views.login, name='login'),
    url(r'^logout/?$', views.logout, name='logout'),
    url(r'^registration/?$', views.registration, name='registration'),

    # url(r'^profile/?$', views.profile, name='profile'),

    url(r'^$', views.index, name='index'),

]
