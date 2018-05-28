from time import sleep
import unittest

from datetime import *

import test as _test
import scrumban_board


class ClientTest(_test.TestCase):
    def test_update_all_reminds(self):
        client = scrumban_board.Client(config_file_path='current_user.cfg')

        user = scrumban_board.User("Roman", "Martyanov", "romamartyanov", "romamartyanov@gmail.com")
        client.client_users.add_new_user(user)

        task = scrumban_board.Task("title", "description")
        task.add_subtask(scrumban_board.Subtask("subtask1"))
        task.add_subtask(scrumban_board.Subtask("subtask2"))

        remind = scrumban_board.Remind(title="Remind", when_remind=datetime.now())

        card = scrumban_board.Card(task=task, users_login=user.login, deadline=remind)

        for board in user.user_boards:
            for cardlist in board.cardlists:
                cardlist.add_card(card)
                break

        raised = False
        try:
            sleep(3)
            while not client.update_all_reminds():
                continue
        except Exception:
            raised = True

        self.assertFalse(raised, 'Exception raised with non-delayed deadline')

    def test_update_all_reminds_more(self):
        client = scrumban_board.Client(config_file_path='current_user.cfg')

        user = scrumban_board.User("Roman", "Martyanov", "romamartyanov", "romamartyanov@gmail.com")
        client.client_users.add_new_user(user)

        task = scrumban_board.Task("title", "description")
        task.add_subtask(scrumban_board.Subtask("subtask1"))
        task.add_subtask(scrumban_board.Subtask("subtask2"))

        remind = scrumban_board.Remind(title="Remind", when_remind=datetime.now(), repeatable_time="minutes=2")
        card = scrumban_board.Card(task=task, users_login=user.login, deadline=remind)

        for board in user.user_boards:
            for cardlist in board.cardlists:
                cardlist.add_card(card)
                break

        raised = False
        try:
            sleep(3)
            while not client.update_all_reminds():
                continue
        except Exception:
            raised = True

        self.assertFalse(raised, 'Exception raised with deadline shift')


if __name__ == "__main__":
    unittest.main()
