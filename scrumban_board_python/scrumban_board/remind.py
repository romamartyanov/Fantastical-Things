from hashlib import sha1
import datetime


class Remind:
    def __init__(self, title=None, description=None, when_remind=None):
        self.title = title
        self.description = description
        self.when_remind = list()

        if when_remind is not None:
            if isinstance(when_remind, datetime.timedelta):
                list.append(self.when_remind, when_remind)

            elif isinstance(when_remind, str):
                pass

        self.id = sha1((title + description + str(datetime.datetime.now())).encode('utf-8'))

    def update_remind(self, title=None, description=None, when_remind=None):
        if title is not None:
            self.title = title

        if description is not None:
            self.description = description

        if when_remind is not None:
            if isinstance(when_remind, datetime.timedelta):
                list.append(self.when_remind, when_remind)

            elif isinstance(when_remind, str):
                pass
