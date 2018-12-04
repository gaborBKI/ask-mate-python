import data_manager
import operator
import time
from datetime import datetime
import database_common


def change_vote(type, direction, type_id):
    questions = get_all_questions()
    answers = get_all_answers()
    if type == 'question':
        for question in questions:
            if question['id'] == int(type_id) and direction == "up":
                update_vote_question(1, type_id)
            elif question['id'] == int(type_id) and direction == "down":
                update_vote(-1, type_id)
    elif type == 'answer':
        for answer in answers:
            if answer['id'] == int(type_id) and direction == "up":
                update_vote_answer(1, type_id)
            elif answer['id'] == int(type_id) and direction == "down":
                update_vote_answer(-1, type_id)


def get_order_by_user(order, questions, status):
    if 'status':
        if order:
            questions = sorted(questions, key=operator.itemgetter(status), reverse=True)
        else:
            questions = sorted(questions, key=operator.itemgetter(status))
    return questions


def get_question_by_user(qid, question_list, title, question, image):
    data = [qid, str(int(time.time())), '0', '0', title, question, image]
    question_list.append(data)
    data_manager.save_into_file(question_list, data_manager.TITLE_LIST_Q, 'question.csv')


def get_answer_by_user(qid):
    answers = data_manager.get_all_data("answer.csv")
    id = util.generate_id(answers)
    data_manager.append_answer_into_file(id, qid, request.form["answertext"])


@database_common.connection_handler
def get_all_questions(cursor):
    cursor.execute("""
                        SELECT * FROM question
                        ORDER BY id;
                       """)
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
    dt = datetime.now()
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
    dt = datetime.now()
    cursor.execute("""
                        INSERT INTO answer (submission_time, vote_number, question_id, message)
                        VALUES (%(dt)s, 0, %(question_id)s, %(message)s);
                       """,
                   {'dt': dt, 'question_id': question_id, 'message': message})
    return None


@database_common.connection_handler
def delete_from_db(cursor, id, tablename):
    cursor.execute(

        sql.SQL("DELETE FROM {table} where id = %(id)s ").
            format(table=sql.Identifier(tablename)), {'id': id})

    return None


@database_common.connection_handler
def delete_question_answers(cursor, qid):
    cursor.execute(""" DELETE FROM answer   WHERE question_id = %(qid)s;
                       DELETE FROM comment   WHERE question_id = %(qid)s;
                       DELETE FROM question_tag   WHERE question_id = %(qid)s;
                        """, {'qid': qid})
    return None


@database_common.connection_handler
def update_vote_question(cursor, direction, type_id):
    cursor.execute(""" UPDATE question
                        SET vote_number = vote_number + %(direction)s
                        WHERE id = %(type_id)s;
                        """, {'direction': direction, 'type_id': type_id})
    return None


@database_common.connection_handler
def update_vote_answer(cursor, direction, type_id):
    cursor.execute(""" UPDATE answer
                        SET vote_number = vote_number + %(direction)s
                        WHERE id = %(type_id)s;
                        """, {'direction': direction, 'type_id': type_id})
    return None
