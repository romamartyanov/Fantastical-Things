from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^login/?$', views.login, name='login'),
    url(r'^logout/?$', views.logout, name='logout'),
    url(r'^registration/?$', views.registration, name='registration'),

    url(r'^$', views.all_boards, name='index'),
    url(r'^board/(?P<board_id>\d+)/?$', views.board, name='board'),

    url(r'^board/(?P<board_id>\d+)/complete_task/(?P<task_id>\d+)/?$', views.complete_task, name='complete_task'),

    url(r'^add_board/?$', views.add_board, name='add_board'),
    url(r'^board/(?P<board_id>\d+)/add_cardlist/?$', views.add_cardlist, name='add_cardlist'),
    url(r'^board/(?P<board_id>\d+)/cardlist/(?P<cardlist_id>\d+)/add_card/?$', views.add_card, name='add_card'),
    url(r'^board/(?P<board_id>\d+)/card/(?P<card_id>\d+)/add_task/?$', views.add_task, name='add_task'),

    url(r'^board/(?P<board_id>\d+)/edit_board/?$', views.edit_board, name='edit_board'),
    url(r'^board/(?P<board_id>\d+)/edit_cardlist/(?P<cardlist_id>\d+)/?$', views.edit_cardlist, name='edit_cardlist'),
    url(r'^board/(?P<board_id>\d+)/edit_card/(?P<card_id>\d+)/?$', views.edit_card, name='edit_card'),
    url(r'^board/(?P<board_id>\d+)/edit_task/(?P<task_id>\d+)/?$', views.edit_task, name='edit_task'),

    url(r'^board/(?P<board_id>\d+)/delete_board/?$', views.delete_board, name='delete_board'),
    url(r'^board/(?P<board_id>\d+)/delete_cardlist/(?P<cardlist_id>\d+)/?$', views.delete_cardlist,
        name='delete_cardlist'),
    url(r'^board/(?P<board_id>\d+)/delete_card/(?P<card_id>\d+)/?$', views.delete_card, name='delete_card'),
    url(r'^board/(?P<board_id>\d+)/delete_task/(?P<task_id>\d+)/?$', views.delete_task, name='delete_task'),

    # url(r'^profile/?$', views.profile, name='profile'),
]
