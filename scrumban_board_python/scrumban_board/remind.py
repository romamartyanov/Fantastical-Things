from hashlib import sha1
from _datetime import *

from scrumban_board_python.scrumban_board.terminal_colors import Colors


class Remind:
    def __init__(self, title: str,
                 when_remind,
                 description: str = None,
                 deadline: bool = None,
                 card_id: str = None,
                 repeating_remind_timedelta: datetime.timedelta = None):

        self.title = title

        if description is not None:
            self.description = description
        else:
            self.description = self.title

        if deadline is not None:
            self.is_deadline = deadline
        else:
            self.is_deadline = False

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
        if repeating_remind_timedelta is not None:
            self.is_repeatable = True
            self.repeating_remind_timedelta = repeating_remind_timedelta

        else:
            self.repeating_remind_timedelta = None

        self.id = sha1(("Remind: " + " " +
                        self.title + " " +
                        str(self.when_remind) + " " +
                        str(datetime.datetime.now())).encode('utf-8'))

    def __str__(self):
        output = Colors.remind_red + """
--- Remind ---
Title: {}
Description: {}
ID: {}
Is Deadline: {}
Is Repeatable: {}
Repeating time delta: {}
--End Remind--
""".format(self.title,
           self.description,
           self.id.hexdigest,
           self.is_deadline,
           self.is_repeatable,
           self.repeating_remind_timedelta) + Colors.end_color

        return output

    def __repr__(self):
        output = Colors.remind_red + """
--- Remind ---
Title: {}
Description: {}
ID: {}
Is Deadline: {}
Is Repeatable: {}
Repeating time delta: {}
--End Remind--
""".format(self.title,
           self.description,
           self.id.hexdigest,
           self.is_deadline,
           self.is_repeatable,
           self.repeating_remind_timedelta) + Colors.end_color

        return output

    def update_remind(self, title: str = None, description: str = None,
                      when_remind=None,
                      repeating_remind_timedelta: datetime.timedelta = None):

        if title is not None:
            self.title = title

        if description is not None:
            self.description = description

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

        if repeating_remind_timedelta is not None:
            self.repeating_remind_timedelta = repeating_remind_timedelta
