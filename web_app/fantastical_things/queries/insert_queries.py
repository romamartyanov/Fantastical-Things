# add_task_start = '''
# INSERT INTO "fantastical_things_task" ("user_id", "title", "description", "status", "begin_time", "card_id")
# VALUES ({user_id},
#         '{title}',
#         '{description}',
#         {status},
#         '{begin_time}'::timestamptz,
#         {card_id}) RETURNING "fantastical_things_task"."id"
# '''
#
# add_task_end = '''
# UPDATE "fantastical_things_task"
# SET "card_id" = {card_id}
# WHERE "fantastical_things_task"."id" IN ({task_id});
#
# INSERT INTO "fantastical_things_task_users" ("task_id", "user_id")
# VALUES ({task_id}, {user_id}) RETURNING "fantastical_things_task_users"."id";
#
#
# UPDATE "fantastical_things_task"
# SET "card_id"     = {card_id}
# WHERE "fantastical_things_task"."id" = {task_id}
#
# '''
