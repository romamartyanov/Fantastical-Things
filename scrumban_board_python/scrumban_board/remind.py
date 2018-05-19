from hashlib import sha1
import datetime


class Remind:
    def __init__(self, title: str,
                 when_remind: datetime.datetime,
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
            self.deadline = deadline
        else:
            self.deadline = False

        if card_id is not None:
            self.card_id = card_id
        else:
            self.card_id = None

        self.when_remind = when_remind

        self.is_repeatable = False
        if repeating_remind_timedelta is not None:
            self.is_repeatable = True
            self.repeating_remind_timedelta = repeating_remind_timedelta

        else:
            self.repeating_remind_timedelta = None

        self.id = sha1(("Remind: " + " " +
                        self.title + " " +
                        self.description + " " +
                        str(self.when_remind) + " " +
                        str(datetime.datetime.now())).encode('utf-8'))

    def update_remind(self, title: str = None, description: str = None,
                      when_remind: datetime.datetime = None,
                      repeating_remind_timedelta: datetime.timedelta = None):

        if title is not None:
            self.title = title

        if description is not None:
            self.description = description

        if when_remind is not None:
            self.when_remind = when_remind

        if repeating_remind_timedelta is not None:
            self.repeating_remind_timedelta = repeating_remind_timedelta
