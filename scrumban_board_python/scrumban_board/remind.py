import os
import logging.config
import string
import random

from hashlib import sha1
from datetime import *
from dateutil.relativedelta import *

from scrumban_board_python.scrumban_board.terminal_colors import Colors

logging.config.fileConfig('logging.cfg')
logger = logging.getLogger("ScrumbanBoard")


class Remind(object):
    """
    Description of Remind

    Example:
    remind = scrumban_board.Remind("Remind", datetime.now(),)

    """

    @staticmethod
    def _get_card_id(card_id=None):
        if card_id is not None:
            return card_id
        else:
            return None

    @staticmethod
    def _get_repeating_remind_relativedelta(repeatable_time=None):
        repeating_remind_relativedelta = None

        if repeatable_time is not None:

            repeatable_time = repeatable_time.split('=')
            unit = repeatable_time[0]
            number = repeatable_time[1]

            if unit == 'years':
                repeating_remind_relativedelta = relativedelta(years=int(number))
            elif number == 'months':
                repeating_remind_relativedelta = relativedelta(months=int(number))
            elif number == 'days':
                repeating_remind_relativedelta = relativedelta(days=int(number))
            elif number == 'hours':
                repeating_remind_relativedelta = relativedelta(hours=int(number))
            elif number == 'minutes':
                repeating_remind_relativedelta = relativedelta(minutes=int(number))

            is_repeatable = True
        else:
            is_repeatable = False

        return repeating_remind_relativedelta, is_repeatable

    @staticmethod
    def _get_when_remind(when_remind):
        """
        Checking correct datetime input

        :param when_remind: datetime/str
        :return: datetime
        """
        if isinstance(when_remind, datetime):
            return when_remind

        elif isinstance(when_remind, str):
            try:
                return datetime.strptime(when_remind, '%Y/%m/%d-%H:%M')

            except ValueError:
                try:
                    return datetime.strptime(when_remind, '%Y/%m/%d')

                except ValueError:
                    return None

        return None

    def __init__(self, title: str, when_remind,
                 description: str = None, card_id: str = None,
                 repeatable_time: str = None):
        """
        Initialising of Remind

        :param title: remind title
        :param when_remind: when remind
        :param description: remind description
        :param card_id: card id of remind
        :param repeatable_time: if remind is periodical
        """

        self.title = title
        self.description = description

        self.card_id = Remind._get_card_id(card_id)

        self.when_remind = self._get_when_remind(when_remind)
        self.repeating_remind_relativedelta, self.is_repeatable = Remind._get_repeating_remind_relativedelta(
            repeatable_time)

        self.id = self._get_id()

        logger.info("Remind ({}) was created".format(self.id))

    def _get_id(self):
        """
        Getting remind id with a help of sha1

        :return: sha1 hash
        """

        key = ''.join(
            random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(len(self.title)))

        return sha1(("Remind: " +
                     self.title + " " +
                     key + " " +
                     str(self.when_remind) + " " +
                     str(datetime.now())).encode('utf-8')).hexdigest()

    def __str__(self):
        output = Colors.remind_red + """
            --- Remind ---
            Title: {}
            Description: {}
            ID: {}
            
            When Remind: {}
            Is Repeatable: {}
            Repeating time delta: {}
            --End Remind--
""".format(self.title,
           self.description,
           self.id,
           self.when_remind,
           self.is_repeatable,
           self.repeating_remind_relativedelta) + Colors.end_color

        return output

    def __repr__(self):
        output = Colors.remind_red + """
            --- Remind ---
            Title: {}
            Description: {}
            ID: {}
            
            When Remind: {}
            Is Repeatable: {}
            Repeating time delta: {}
            --End Remind--
""".format(self.title,
           self.description,
           self.id,
           self.when_remind,
           self.is_repeatable,
           self.repeating_remind_relativedelta) + Colors.end_color

        return output

    def update_remind(self, title: str = None, description: str = None, card_id: str = None,
                      when_remind=None,
                      repeating_remind_relativedelta: relativedelta = None):
        """
        Updating of Remind


        :param title: remind title
        :param when_remind: when remind
        :param description: remind description
        :param card_id: card id of remind
        :param repeating_remind_relativedelta: if remind is periodical
        :return:
        """

        if title is not None:
            self.title = title

        if description is not None:
            self.description = description

        if card_id is not None:
            self.card_id = Remind._get_card_id(card_id)

        if when_remind is not None:
            self.when_remind = Remind._get_when_remind(when_remind)

        if repeating_remind_relativedelta is not None:
            self.repeating_remind_relativedelta, self.is_repeatable = Remind._get_repeating_remind_relativedelta(
                repeating_remind_relativedelta)

        logger.info("Remind ({}) was updated".format(self.id))
