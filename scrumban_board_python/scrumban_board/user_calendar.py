from collections import deque


class UserCalendar:
    def __init__(self, user_id=None):
        self.user_id = user_id

        self.past_reminds = deque()
        self.future_reminds = deque()

    def update_queues(self):
        pass

    def add_to_queues(self):
        pass

    def remove_from_queues(self):
        pass

    # def add_remind(self, remind):
    #     self.reminds_list.append(remind)
    #
    # def remove_remind(self, remind=None, remind_id=None):
    #     if remind is not None:
    #         self.reminds_list.remove(remind)
    #
    #     elif remind_id is not None:
    #         if remind_id is not None:
    #             remind = next(remind for remind in self.reminds_list if remind.id == remind_id)
    #             self.reminds_list.remove(remind)
    #
    # def find_remind(self, title=None, remind_id=None):
    #     if remind_id is not None:
    #         return next(remind for remind in self.reminds_list if remind.id == remind_id)
    #
    #     elif title is not None:
    #         return next(remind for remind in self.reminds_list if remind.title == title)
    #
    # def update_past_future_reminds(self, now_time):
