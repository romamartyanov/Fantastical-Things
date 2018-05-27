import argparse
import logging.config

from scrumban_board_python import scrumban_board

logging.config.fileConfig('console_handler_logging.cfg')
logger = logging.getLogger("ConsoleHandler")


class ConsoleHandler:
    parser = argparse.ArgumentParser()
    client = scrumban_board.Client(config_file_path='current_user.cfg')

    user = scrumban_board.User("Roman", "Martyanov", "romamartyanov", "romamartyanov@gmail.com")
    client.client_users.add_new_user(user)

    parser.add_argument("--create_card", help="add card")
    args = parser.parse_args()
    if args.create_card:
        print(scrumban_board.Card(args.create_card, user))
