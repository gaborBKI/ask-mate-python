from datetime import datetime
import database_common
from psycopg2 import sql
import data_manager

@database_common.connection_handler
def get_all_questions_desc(cursor, order_by_what):
    cursor.execute(sql.SQL(""" SELECT * FROM question
                            ORDER BY {order_by_what} DESC;
                            """).format(order_by_what=sql.Identifier(order_by_what)))
    questions = cursor.fetchall()
    for question in questions:
        question['comments'] = get_all_comments('question', question['id'])
        question['answers'] = data_manager.get_answers_to_question(get_all_answers(), question['id'])

    return questions


@database_common.connection_handler
def get_all_questions_asc(cursor, order_by_what):
    cursor.execute(sql.SQL(""" SELECT * FROM question
                            ORDER BY {order_by_what} ASC;
                            """).format(order_by_what=sql.Identifier(order_by_what)))
    questions = cursor.fetchall()
    for question in questions:
        question['comments'] = get_all_comments('question', question['id'])
        question['answers'] = data_manager.get_answers_to_question(get_all_answers(), question['id'])
    return questions


@database_common.connection_handler
def get_all_questions(cursor, order_by_what, searchvalue, limit):
    '''    query = 'SELECT * FROM question'
        if limit:
            query += ' LIMIT'

            query += " ORDER BY {order_by_what} DESC".format(order_by_what=sql.Identifier(order_by_what))'''
    if not searchvalue and limit:
        cursor.execute(sql.SQL(""" SELECT * FROM question
                                ORDER BY {order_by_what} DESC limit 5;
                                """).format(order_by_what=sql.Identifier(order_by_what)))
    elif not searchvalue and not limit:
        cursor.execute(sql.SQL(""" SELECT * FROM question
                                ORDER BY {order_by_what};
                                """).format(order_by_what=sql.Identifier(order_by_what)))
    else:

        cursor.execute(sql.SQL(""" SELECT * FROM question where title like %(searchvalue)s or message like %(searchvalue)s 
                                    or id in (select question_id from answer where answer.message like  %(searchvalue)s)
                                                ORDER BY {order_by_what};

                                                """).format(order_by_what=sql.Identifier(order_by_what)),
                       {'searchvalue': searchvalue})

    questions = cursor.fetchall()
    for question in questions:
        question['comments'] = get_all_comments('question', question['id'])
        question['answers'] = data_manager.get_answers_to_question(get_all_answers(), question['id'])

    return questions


@database_common.connection_handler
def get_all_answers(cursor):
    cursor.execute("""
                        SELECT answer.id, answer.submission_time, answer.vote_number, answer.question_id, answer.message, answer.image, answer.user_id, users.username, users.id as user_id FROM answer JOIN users on answer.user_id = users.id
                        ORDER BY answer.id;
                       """)
    answers = cursor.fetchall()
    return answers


@database_common.connection_handler
def get_all_comments(cursor, qa_type, qa_id):
    if qa_type == 'question':
        cursor.execute("""
                            SELECT comment.id, question_id, message, submission_time, username, u.id as user_id
                            FROM comment LEFT JOIN users u on comment.user_id = u.id
                            WHERE question_id = %(qa_id)s
                            ORDER BY submission_time DESC;
                        """, {'qa_id': qa_id})
    else:
        cursor.execute("""
                            SELECT comment.id, answer_id, message, submission_time, username, u.id as user_id
                            FROM comment LEFT JOIN users u on comment.user_id = u.id
                            WHERE answer_id = %(qa_id)s
                            ORDER BY submission_time DESC;
                        """, {'qa_id': qa_id})
    comments = cursor.fetchall()
    return comments


@database_common.connection_handler
def add_comment(cursor, qa_type, qa_id, text, uid):
    dt = str(datetime.now())[:19]
    cursor.execute(sql.SQL("""
                        INSERT INTO comment
                        ({qa_type}, message, submission_time, user_id)
                        VALUES (%(qa_id)s, %(text)s, %(dt)s, %(uid)s)
                    """).format(qa_type=sql.Identifier(qa_type)), {'qa_id': qa_id, 'text': text, 'dt': dt, 'uid': uid})
    return None


@database_common.connection_handler
def add_question(cursor, q_title, question, im_link, uid):
    dt = str(datetime.now())[:19]
    cursor.execute("""
                        INSERT INTO question (submission_time, view_number, vote_number, title, message, image, user_id)
                        VALUES (%(dt)s, 0, 0, %(q_title)s, %(question)s, %(im_link)s, %(uid)s);-- RETURNING id;
                        SELECT id FROM question WHERE id=(SELECT max(id) FROM question);
                       """,
                   {'dt': dt, 'q_title': q_title, 'question': question, 'im_link': im_link, 'uid': uid})
    submitted_question = cursor.fetchone()
    return submitted_question


@database_common.connection_handler
def add_answer(cursor, question_id, message, uid):
    dt = str(datetime.now())[:19]
    cursor.execute("""
                        INSERT INTO answer (submission_time, vote_number, question_id, message, user_id)
                        VALUES (%(dt)s, 0, %(question_id)s, %(message)s, %(uid)s);
                       """,
                   {'dt': dt, 'question_id': question_id, 'message': message, 'uid': uid})
    return None


@database_common.connection_handler
def delete_from_db(cursor, id, tablename, var_id):
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


@database_common.connection_handler
def get_style(cursor, usname):
    cursor.execute("""
                        SELECT style FROM users where username = %(usname)s
                       """, {'usname': usname})
    style = cursor.fetchone()
    return style


@database_common.connection_handler
def make_style(cursor, colour, usname):
    cursor.execute(""" UPDATE users SET style = %(colour)s where username = %(usname)s;
                        """, {'colour': colour, 'usname': usname})
    return None


@database_common.connection_handler
def register_user(cursor, username, password, profile_picture):
    dt = str(datetime.now())[:19]
    cursor.execute("""
                        INSERT INTO users (registered, username, password, profile_picture)
                        VALUES (%(dt)s, %(username)s, %(password)s, %(profile_picture)s);
                       """,
                   {'dt': dt, 'username': username, 'password': password, 'profile_picture': profile_picture})
    return None


@database_common.connection_handler
def get_user_password(cursor, username):
    cursor.execute("""
                        SELECT password FROM users
                        WHERE username = %(username)s;
                       """,
                   {'username': username})
    password = cursor.fetchone()
    return password


@database_common.connection_handler
def get_all_users(cursor):
    cursor.execute("""
                        SELECT username, registered, id FROM users;
                       """)
    usernames = cursor.fetchall()
    return usernames


@database_common.connection_handler
def get_user(cursor, userid):
    cursor.execute("""
                        SELECT id, username, registered, profile_picture FROM users
                        WHERE id = %(userid)s;
                       """,
                   {'userid': userid})
    userdata = cursor.fetchone()
    return userdata

  
@database_common.connection_handler
def get_questions_by_user(cursor, userid):
    cursor.execute("""
                        SELECT id, title FROM question
                        WHERE user_id = %(userid)s
                        ORDER BY submission_time DESC;
                       """,
                   {'userid': userid})
    questions = cursor.fetchall()
    return questions


@database_common.connection_handler
def get_answers_by_user(cursor, userid):
    cursor.execute("""
                        SELECT id, message, question_id FROM answer
                        WHERE user_id = %(userid)s
                        ORDER BY submission_time DESC;
                       """,
                   {'userid': userid})
    questions = cursor.fetchall()
    return questions


@database_common.connection_handler
def get_comments_by_user(cursor, userid):
    cursor.execute("""
                        SELECT comment.id, comment.message, comment.question_id, answer_id, answer.question_id AS qid FROM comment LEFT JOIN answer on comment.answer_id = answer.id
                        WHERE comment.user_id = %(userid)s
                        ORDER BY comment.submission_time DESC;
                       """,
                   {'userid': userid})
    comments = cursor.fetchall()
    return comments


@database_common.connection_handler
def get_user_by_name(cursor, username):
    cursor.execute("""
                        SELECT id, registered, profile_picture FROM users
                        WHERE username = %(username)s;
                       """,
                   {'username': username})
    userdata = cursor.fetchone()
    return userdata
