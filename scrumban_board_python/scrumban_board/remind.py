from hashlib import sha1
import datetime


class Remind:
    def __init__(self, title=None, description=None, when_remind=None, repeating_remind_timedelta=None):
        if title is not None:
            self.title = title
        else:
            self.title = "Remind at " + str(datetime.datetime.now())

        if description is not None:
            self.description = description
        else:
            self.description = "Remind at " + str(datetime.datetime.now())

        self.is_repeatable = False

        if when_remind is not None:
            if isinstance(when_remind, datetime.datetime):
                self.when_remind = when_remind

            elif isinstance(when_remind, str):
                pass

        else:
            self.when_remind = datetime.datetime.now()

        if repeating_remind_timedelta is not None:
            self.is_repeatable = True

            if isinstance(repeating_remind_timedelta, datetime.timedelta):
                self.repeating_remind_timedelta = repeating_remind_timedelta

            elif isinstance(repeating_remind_timedelta, str):
                pass

        else:
            self.repeating_remind_timedelta = repeating_remind_timedelta

        self.id = sha1(("Remind: " + " " +
                        self.title + " " +
                        self.description + " " +
                        str(datetime.datetime.now())).encode('utf-8'))

    def update_remind(self, title=None, description=None, when_remind=None, repeating_remind_timedelta=None):
        if title is not None:
            self.title = title

        if description is not None:
            self.description = description

        if when_remind is not None:
            if isinstance(when_remind, datetime.datetime):
                self.when_remind = when_remind

            elif isinstance(when_remind, str):
                pass

        if repeating_remind_timedelta is not None:
            if isinstance(repeating_remind_timedelta, datetime.timedelta):
                self.repeating_remind_timedelta = repeating_remind_timedelta

            elif isinstance(repeating_remind_timedelta, str):
                pass