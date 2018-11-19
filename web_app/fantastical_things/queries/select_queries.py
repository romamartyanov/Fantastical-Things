### ALL

all_user_boards = '''SELECT *
        FROM "fantastical_things_board"
                       INNER JOIN "fantastical_things_board_users"
                         ON ("fantastical_things_board"."id" = "fantastical_things_board_users"."board_id")
        WHERE "fantastical_things_board_users"."user_id" = {user_id}'''

all_card_lists_on_board = '''
SELECT *
FROM "fantastical_things_cardlist"
       INNER JOIN "fantastical_things_cardlist_users"
         ON ("fantastical_things_cardlist"."id" = "fantastical_things_cardlist_users"."cardlist_id")
WHERE ("fantastical_things_cardlist"."board_id" = {board_id} AND "fantastical_things_cardlist_users"."user_id" = {user_id})'''

all_boards_users = '''SELECT *
FROM "auth_user"
       INNER JOIN "fantastical_things_board_users" ON ("auth_user"."id" = "fantastical_things_board_users"."user_id")
WHERE "fantastical_things_board_users"."board_id" = {board_id}'''

all_cards_in_cardlist = '''SELECT *
FROM "fantastical_things_card"
       INNER JOIN "fantastical_things_card_users"
         ON ("fantastical_things_card"."id" = "fantastical_things_card_users"."card_id")
WHERE ("fantastical_things_card"."cardlist_id" = {cardlist_id} AND "fantastical_things_card_users"."user_id" = {user_id})'''

all_tasks_in_card = '''SELECT *
FROM "fantastical_things_task"
       INNER JOIN "fantastical_things_task_users"
         ON ("fantastical_things_task"."id" = "fantastical_things_task_users"."task_id")
WHERE ("fantastical_things_task"."card_id" = {card_id} AND "fantastical_things_task_users"."user_id" = {user_id})'''

###

all_card_lists_on_updating = '''
SELECT *
FROM "fantastical_things_cardlist"
WHERE "fantastical_things_cardlist"."board_id" = {board_id}
'''

all_cards_on_updating = '''SELECT *
FROM "fantastical_things_card"
WHERE "fantastical_things_card"."cardlist_id" = {cardlist_id}'''

### ONE
