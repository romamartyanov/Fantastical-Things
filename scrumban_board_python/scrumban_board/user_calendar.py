from collections import deque
import datetime

from scrumban_board_python.scrumban_board.remind import Remind


class Calendar:
    def __init__(self, users_id, reminds: deque = None):

        self.users_id = deque()
        if isinstance(users_id, str):
            self.users_id.append(users_id)

        elif isinstance(users_id, deque):
            for user_id in users_id:
                if isinstance(user_id, str):
                    self.users_id.append(user_id)

        self.future_reminds = deque()

        if reminds is not None:
            for remind in reminds:
                self.add_to_deque(remind)

    def find_in_deque(self, remind_id: str):
        try:
            found_remind = next(remind for remind in self.future_reminds if remind.id == remind_id)
        except ValueError:
            return None

        return found_remind

    def add_to_deque(self, remind: Remind):
        if len(self.future_reminds) == 0:
            self.future_reminds.appendleft(remind)

        else:
            for deque_remind in self.future_reminds:
                if deque_remind.when_remind > remind.when_remind:
                    self.future_reminds.insert(self.future_reminds.index(deque_remind), remind)
                    break

            else:
                self.future_reminds.append(remind)

    def remove_from_deque(self, remind: Remind):
        found_remind = self.find_in_deque(remind.id)
        if found_remind is not None:
            self.future_reminds.remove(found_remind)

    def update_deque(self, remind: Remind):
        found_remind = self.find_in_deque(remind.id)

        if found_remind is not None:
            self.future_reminds.remove(found_remind)
            self.add_to_deque(remind)

    def check_deque(self):
        for deque_remind in self.future_reminds:
            if deque_remind.when_remind < datetime.datetime.now():
                    # do something with remind

                    self.future_reminds.popleft()

            else:
                break
