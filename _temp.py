from scrumban_board_python import scrumban_board

from hashlib import sha1
import datetime

name = "name"
surname = "surname"

m = sha1((name+surname).encode('utf-8'))

print(m.hexdigest())
print()

d = {}

d[[1]] = 'a'
d[[2]] = 'b'

print(d[[1]])

# rem = scrumban_board.Remind()
# rem.update_remind(title=name, description=surname, when_remind="d")
