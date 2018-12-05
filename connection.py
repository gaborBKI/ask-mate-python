from datetime import datetime
import database_common
from psycopg2 import sql


@database_common.connection_handler
def get_all_questions_desc(cursor, order_by_what):
    cursor.execute(sql.SQL(""" SELECT * FROM question
                            ORDER BY {order_by_what} DESC;
                            """).format(order_by_what=sql.Identifier(order_by_what)))
    questions = cursor.fetchall()
    return questions


@database_common.connection_handler
def get_all_questions_asc(cursor, order_by_what):
    cursor.execute(sql.SQL(""" SELECT * FROM question
                            ORDER BY {order_by_what} ASC;
                            """).format(order_by_what=sql.Identifier(order_by_what)))
    questions = cursor.fetchall()
    return questions


@database_common.connection_handler
def get_all_questions(cursor, order_by_what, searchvalue, limit):
    if not searchvalue:
        cursor.execute(sql.SQL(""" SELECT * FROM question
                                ORDER BY {order_by_what} limit 5;
                                """).format(order_by_what=sql.Identifier(order_by_what)))
    else:

        cursor.execute(sql.SQL(""" SELECT * FROM question where title like %(searchvalue)s or message like %(searchvalue)s 
                                    or id in (select question_id from answer where answer.message like  %(searchvalue)s)
                                                ORDER BY {order_by_what};

                                                """).format(order_by_what=sql.Identifier(order_by_what)),
                       {'searchvalue': searchvalue})

    questions = cursor.fetchall()
    return questions


@database_common.connection_handler
def get_all_answers(cursor):
    cursor.execute("""
                        SELECT * FROM answer
                        ORDER BY id;
                       """)
    answers = cursor.fetchall()
    return answers


@database_common.connection_handler
def add_question(cursor, q_title, question, im_link):
    dt = str(datetime.now())[:19]
    cursor.execute("""
                        INSERT INTO question (submission_time, view_number, vote_number, title, message, image)
                        VALUES (%(dt)s, 0, 0, %(q_title)s, %(question)s, %(im_link)s);
                        SELECT id FROM question WHERE id=(SELECT max(id) FROM question);
                       """,
                   {'dt': dt, 'q_title': q_title, 'question': question, 'im_link': im_link})
    submitted_question = cursor.fetchall()
    return submitted_question


@database_common.connection_handler
def add_answer(cursor, question_id, message):
    dt = str(datetime.now())[:19]
    cursor.execute("""
                        INSERT INTO answer (submission_time, vote_number, question_id, message)
                        VALUES (%(dt)s, 0, %(question_id)s, %(message)s);
                       """,
                   {'dt': dt, 'question_id': question_id, 'message': message})
    return None


@database_common.connection_handler
def delete_from_db(cursor, id, tablename, var_id):
    print(id)
    if tablename == "question":
        delete_from_db(id, 'comment', 'question_id')
        delete_from_db(id, 'answer', 'question_id')
        delete_from_db(id, 'question_tag', 'question_id')

    elif tablename == "answer":
        delete_from_db(id, 'comment', 'answer_id')

    cursor.execute(

        sql.SQL("DELETE FROM {table} where {varid} = %(id)s ").
            format(table=sql.Identifier(tablename), varid=sql.Identifier(var_id)), {'id': id})

    return None


@database_common.connection_handler
def update_vote(cursor, tablename, direction, type_id):
    cursor.execute(sql.SQL(""" UPDATE {table}
                        SET vote_number = vote_number + %(direction)s
                        WHERE id = %(type_id)s;
                        """).format(table=sql.Identifier(tablename)), {'direction': direction, 'type_id': type_id})
    return None


@database_common.connection_handler
def update_view_number(cursor, qid):
    cursor.execute(""" UPDATE question SET view_number = view_number + 1
                        WHERE id = %(qid)s;
                        """, {'qid': qid})
    return None


@database_common.connection_handler
def update_question_text(cursor, qid, edited_text):
    cursor.execute(""" UPDATE question SET message = %(edited_text)s
                        WHERE id = %(qid)s;
                        """, {'qid': qid, 'edited_text': edited_text})
    return None
