from hashlib import sha1
from datetime import *
from dateutil.relativedelta import *

from scrumban_board_python.scrumban_board.terminal_colors import Colors


class Remind:
    """
    Description of Remind

    Example:
    remind = scrumban_board.Remind(client.logger, "Remind", datetime.now(),

    """
    def __init__(self, logger,  title: str, when_remind,
                 description: str = None, card_id: str = None,
                 repeating_remind_relativedelta: relativedelta = None):
        """
        Initialising of Remind

        :param logger: client logger
        :param title: remind title
        :param when_remind: when remind
        :param description: remind description
        :param card_id: card id of remind
        :param repeating_remind_relativedelta: if remind is periodical
        """

        self.title = title
        self.logger = logger

        if description is not None:
            self.description = description
        else:
            self.description = self.title

        if card_id is not None:
            self.card_id = card_id
        else:
            self.card_id = None

        try:
            self.when_remind = when_remind
        except ValueError:
            try:
                self.when_remind = datetime.strptime(when_remind, '%Y/%m/%d %H:%M')
            except ValueError:
                try:
                    self.when_remind = datetime.strptime(when_remind, '%Y/%m/%d')
                except ValueError:
                    self.when_remind = datetime.now()

        self.is_repeatable = False
        if repeating_remind_relativedelta is not None:
            self.is_repeatable = True
            self.repeating_remind_relativedelta = repeating_remind_relativedelta

        else:
            self.repeating_remind_relativedelta = None

        self.id = sha1(("Remind: " + " " +
                        self.title + " " +
                        str(self.when_remind) + " " +
                        str(datetime.now())).encode('utf-8')).hexdigest()

        self.logger.info("Remind ({}) was created".format(self.id))

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
            self.card_id = card_id
        else:
            self.card_id = None

        if when_remind is not None:
            try:
                self.when_remind = when_remind
            except ValueError:
                try:
                    self.when_remind = datetime.strptime(when_remind, '%Y/%m/%d %H:%M')
                except ValueError:
                    try:
                        self.when_remind = datetime.strptime(when_remind, '%Y/%m/%d')
                    except ValueError:
                        self.when_remind = datetime.now()

        if repeating_remind_relativedelta is not None:
            self.is_repeatable = True
            self.repeating_remind_relativedelta = repeating_remind_relativedelta

        self.logger.info("Remind ({}) was updated".format(self.id))
