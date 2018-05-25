from collections import deque
from datetime import *
from dateutil.relativedelta import *
import time


# from hashlib import sha1
# import datetime
#
# name = "name"
# surname = "surname"
#
# m = sha1((name+surname).encode('utf-8'))
#
# print(m.hexdigest())
# print()
#
# d = {}
#
# d[[1]] = 'a'
# d[[2]] = 'b'
#
# print(d[[1]])

# rem = scrumban_board.Remind()
# rem.update_remind(title=name, description=surname, when_remind="d")
# a = list([scrumban_board.User(name="1"), scrumban_board.User(name="2")])
#
# print(next(user for user in a if user.name == "3"))

# a = deque()
#
# a.append(2)
# a.append(4)
# a.append(5)
# print(a)
#
# a.insert(a.index(4), 3)
# print(a)
#
# for i in a:
#     print(i)

# NOW = datetime.now()
# b = date(2017, 9, 5)
#
# # if NOW > b:
# #     print(NOW)
#
# NOW = NOW+relativedelta(minutes=+10)
# print(NOW)

# dt = datetime.strptime("2019/10/20 12:00", '%Y/%m/%d')
# print(dt)
#
#
# u = scrumban_board.User("Roman", "Martyanov", "romamartyanov", "romamartyanov@gmail.com")
#
# t = scrumban_board.Task("title", "description")
# t.add_subtask(scrumban_board.Subtask("subtask1"))
# t.add_subtask(scrumban_board.Subtask("subtask2"))
#
# r = scrumban_board.Remind("Remind", datetime.now())
# c = scrumban_board.Card(t, u.id)
#
# r_l = deque()
# r_l.append(r)
#
# c.update_card(reminds_list=r_l)
# print(u)
# print(c)

# print (scrumban_board.BColors.WARNING + "Warning:" + scrumban_board.BColors.HEADER +
#        "No active" + scrumban_board.BColors.CYAN + "frommets" + scrumban_board.BColors.GREEN +
#        "remain." + scrumban_board.BColors.FAIL+" Continue?"
#       + scrumban_board.BColors.ENDC)

# t1 = datetime.now() + timedelta(seconds=1)
# time.sleep(3)
#
# if t1 < datetime.now():
#     print(True)

from scrumban_board_python import scrumban_board

client = scrumban_board.Client()

user = scrumban_board.User("Roman", "Martyanov", "romamartyanov", "romamartyanov@gmail.com")
client.client_users.add_new_user(user)

task = scrumban_board.Task("title", "description")
task.add_subtask(scrumban_board.Subtask("subtask1"))
task.add_subtask(scrumban_board.Subtask("subtask2"))

remind = scrumban_board.Remind("Remind", datetime.now(),
                               )

card = scrumban_board.Card(task=task, users_login=user.login, deadline=remind, reminds_list=remind)

remind_list = deque()
remind_list.append(remind)

card.update_card(reminds_list=remind_list)

for board in user.user_boards:
    for cardlist in board.cardlists:
        cardlist.add_card(card)
        break

time.sleep(3)
while not client.update_all_reminds():
    continue

import json
import jsonpickle

frozen = jsonpickle.encode(client)
with open('client.json', 'w') as outfile:
    json.dump(frozen, outfile)


with open('client.json') as infile:
    data = json.load(infile)

client = jsonpickle.decode(data)

# import pickle
#
# with open('client.json', 'wb') as pickle_file:
#     pickle.dump(client, pickle_file)
#
# with open('client.json', 'rb') as pickle_file:
#     client = pickle.load(pickle_file)

while not client.update_all_reminds():
    continue

for board in user.user_boards:
    print(board)




