quit_board = '''
DELETE
FROM "fantastical_things_board_users"
WHERE ("fantastical_things_board_users"."board_id" = {board_id} AND "fantastical_things_board_users"."user_id" IN ({user_id}));


UPDATE "fantastical_things_board"
SET "user_id"     = 1
WHERE "fantastical_things_board"."id" = {board_id};

'''

delete_task = '''
DELETE
FROM "fantastical_things_task_users"
WHERE "fantastical_things_task_users"."task_id" IN ({task_id});

DELETE
FROM "fantastical_things_task"
WHERE "fantastical_things_task"."id" IN ({task_id});


'''

delele_card = '''
'''

delele_cardlist = '''
'''

delete_board = '''
'''
