import argparse

from scrumban_board_python import scrumban_board


class Handler:
    parser = argparse.ArgumentParser()
    client = scrumban_board.Client()

    user = scrumban_board.User(client.logger, "Roman", "Martyanov", "romamartyanov", "romamartyanov@gmail.com")
    client.client_users.add_new_user(user)

    parser.add_argument("--create_card", help="add card")
    args = parser.parse_args()
    if args.create_card:
        print(scrumban_board.Card(client.logger, args.create_card, user))
