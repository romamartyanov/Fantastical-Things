from datetime import *
from dateutil.relativedelta import *

import time
import json

import jsonpickle

from scrumban_board_python import scrumban_board

client = scrumban_board.Client(config_file_path='current_user.cfg')

user = scrumban_board.User("Roman", "Martyanov", "romamartyanov", "romamartyanov@gmail.com")
client.client_users.add_new_user(user)

task = scrumban_board.Task("title", "description")
task.add_subtask(scrumban_board.Subtask("subtask1"))
task.add_subtask(scrumban_board.Subtask("subtask2"))

remind = scrumban_board.Remind(title="Remind", when_remind=datetime.now(),
                               repeating_remind_relativedelta=relativedelta(hours=+2))

card = scrumban_board.Card(task=task, users_login=user.login, deadline=remind)

for board in user.user_boards:
    for cardlist in board.cardlists:
        cardlist.add_card(card)
        break

time.sleep(3)
while not client.update_all_reminds():
    continue


frozen = jsonpickle.encode(client)
with open('client.json', 'w') as outfile:
    json.dump(frozen, outfile)

with open('client.json', 'r') as infile:
    data = json.load(infile)

client = jsonpickle.decode(data)

while not client.update_all_reminds():
    continue

for board in user.user_boards:
    print(board)

# import console_handler
#
# console_handler.Handler()
