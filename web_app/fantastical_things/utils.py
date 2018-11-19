from .models import *
from fantastical_things.queries import select_queries

import datetime
import dateutil.parser
from dateutil.relativedelta import *


def add_user_to_all_tasks(board, new_user):
    card_lists = board.cardlist_set.all()

    for card_list in card_lists:
        cards = card_list.card_set.all()

        for card in cards:
            tasks = card.task_set.all()

            for task in tasks:
                task.users.add(new_user)
                task.save()

            card.users.add(new_user)
            card.save()

        card_list.users.add(new_user)
        card_list.save()


def update_cards(board):
    # card_lists = board.cardlist_set.all()
    card_lists = board.cardlist_set.raw(select_queries.all_card_lists_on_updating.format(board_id=board.id))

    overdue = None
    to_do = None

    # try:
    for card_list in card_lists:
        if card_list.title == 'Overdue':
            overdue = card_list
        elif card_list.title == 'To-Do':
            to_do = card_list

    if overdue is None or to_do is None:
        return

        # overdue_cardlist = board.cardlist_set.get(title='Overdue')
        # to_do = board.cardlist_set.get(title='To-Do')

    # except CardList.DoesNotExist:
    #     return

    for card_list in card_lists:
        cards = card_list.card_set.all()
        cards = card_list.card_set.raw(select_queries.all_cards_on_updating.format(cardlist_id=card_list.id))

        for card in cards:
            if card.deadline is not None:
                deadline = card.deadline
                deadline = deadline.replace(tzinfo=None)

                if deadline < datetime.datetime.now() + datetime.timedelta(hours=3):
                    if card.repeatable:
                        time_delta = relativedelta(years=+int(card.years),
                                                   months=+int(card.months),
                                                   days=+int(card.days),
                                                   hours=+int(card.hours),
                                                   minutes=+int(card.minutes),
                                                   seconds=+int(card.seconds))

                        new_deadline = deadline + time_delta
                        while new_deadline < datetime.datetime.now() + datetime.timedelta(hours=3):
                            new_deadline = new_deadline + time_delta

                        q = Card.objects.filter(id=card.id).update(deadline=new_deadline)
                        print(q.query)
                        q = Card.objects.filter(id=card.id).update(cardlist=to_do)
                        print(q.query)

                    else:
                        q = Card.objects.filter(id=card.id).update(cardlist=overdue)
                        print(q.query)