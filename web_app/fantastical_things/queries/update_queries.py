set_task_status = '''
UPDATE "fantastical_things_task"
SET "status" = {status}
WHERE "fantastical_things_task"."id" IN (SELECT U0."id"
                                         FROM "fantastical_things_task" U0
                                                INNER JOIN "fantastical_things_task_users" U1
                                                  ON (U0."id" = U1."task_id")
                                         WHERE (U0."id" = {task_id} AND U1 . "user_id" = {user_id}))
'''

set_board_info = '''
UPDATE "fantastical_things_board"
SET "description" = '{new_description}',
    "title"       = '{new_title}'
WHERE "fantastical_things_board"."id" IN (SELECT U0."id"
                                          FROM "fantastical_things_board" U0
                                                 INNER JOIN "fantastical_things_board_users" U1
                                                   ON (U0."id" = U1."board_id")
                                          WHERE (U0."id" = {board_id} AND U1 . "user_id" = {user_id}));
'''

set_cardlist_info = '''
UPDATE "fantastical_things_cardlist"
SET "title"       = '{new_title}',
    "description" = '{new_description}'
WHERE "fantastical_things_cardlist"."id" IN (SELECT U0."id"
                                             FROM "fantastical_things_cardlist" U0
                                                    INNER JOIN "fantastical_things_cardlist_users" U1
                                                      ON (U0."id" = U1."cardlist_id")
                                             WHERE (U0."id" = {cardlist_id} AND U1 . "user_id" = {user_id}));
'''


set_card_title_info = '''
UPDATE "fantastical_things_card"
SET "title" = '{card_title}'
WHERE "fantastical_things_card"."id" IN (SELECT U0."id"
                                         FROM "fantastical_things_card" U0
                                                INNER JOIN "fantastical_things_card_users" U1
                                                  ON (U0."id" = U1."card_id")
                                         WHERE (U0."id" = {card_id} AND U1."user_id" = {user_id}));
'''

set_card_cardlist = '''
UPDATE "fantastical_things_card"
SET "cardlist_id" = {cardlist_id}
WHERE "fantastical_things_card"."id" IN (SELECT U0."id"
                                         FROM "fantastical_things_card" U0
                                                INNER JOIN "fantastical_things_card_users" U1
                                                  ON (U0."id" = U1."card_id")
                                         WHERE (U0."id" = {card_id} AND U1."user_id" = {user_id}));
'''

set_card_deadline = '''
UPDATE "fantastical_things_card"
SET "deadline" = '{deadline}' :: timestamptz
WHERE "fantastical_things_card"."id" IN (SELECT U0."id"
                                         FROM "fantastical_things_card" U0
                                                INNER JOIN "fantastical_things_card_users" U1
                                                  ON (U0."id" = U1."card_id")
                                         WHERE (U0."id" = {card_id} AND U1."user_id" = {user_id}));


'''

set_repeatable_card = '''
UPDATE "fantastical_things_card"
SET "seconds"    = {seconds},
    "months"     = {months},
    "minutes"    = {minutes},
    "days"       = {days},
    "years"      = {years},
    "repeatable" = {repeatable},
    "hours"      = {hours}
WHERE "fantastical_things_card"."id" IN (SELECT U0."id"
                                         FROM "fantastical_things_card" U0
                                                INNER JOIN "fantastical_things_card_users" U1
                                                  ON (U0."id" = U1."card_id")
                                         WHERE (U0."id" = {card_id} AND U1."user_id" = {user_id}));
'''

set_task_info = '''
UPDATE "fantastical_things_task"
SET "title"       = '{new_title}',
    "description" = '{new_description}',
    "status"      = {new_status}
    WHERE
    "fantastical_things_task"."id" IN (
    SELECT
    U0."id"
    FROM
    "fantastical_things_task" U0
    INNER JOIN
    "fantastical_things_task_users" U1 ON (U0."id" = U1."task_id")
    WHERE
    (U0."id" = {task_id} AND U1."user_id" = {user_id}));
'''

