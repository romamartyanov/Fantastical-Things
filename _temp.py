from collections import deque
import datetime

from scrumban_board_python import scrumban_board

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

a = datetime.datetime.now()
b = datetime.datetime(2017, 9, 5)

if a > b:
    print(a)

