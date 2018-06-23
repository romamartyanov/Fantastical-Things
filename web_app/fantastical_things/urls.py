from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^login/?$', views.login, name='login'),
    url(r'^logout/?$', views.logout, name='logout'),
    url(r'^registration/?$', views.registration, name='registration'),

    url(r'^$', views.all_boards, name='index'),
    url(r'^board/(?P<board_id>\d+)/?$', views.board, name='board'),

    url(r'^board/(?P<board_id>\d+)/complete_task/(?P<task_id>\d+)/?$', views.complete_task, name='complete_task'),
    # url(r'^incomplete_task/(?P<task_id>\d+)/?&', views.incomplete_task, name='incomplete_task')

    # url(r'^add_board/?$', views.add_board, name='add_board'),
    # url(r'^add_cardlist/?$', views.add_cardlist, name='add_cardlist'),
    # url(r'^add_card/?$', views.add_card, name='add_card'),
    # url(r'^add_task/?$', views.add_task, name='add_task'),

    # url(r'^edit_board/?$', views.edit_board, name='edit_board'),
    # url(r'^edit_cardlist/?$', views.edit_cardlist, name='edit_cardlist'),
    # url(r'^edit_card/?$', views.edit_card, name='edit_card'),
    # url(r'^edit_task/?$', views.edit_task, name='edit_task'),

    # url(r'^profile/?$', views.profile, name='profile'),
]
