import data_manager
import operator
import time
from datetime import datetime
import database_common
import util


def change_vote(type, direction, type_id):
    data = data_manager.get_all_data(f'{type}.csv')
    if type == 'question':
        title_list = data_manager.TITLE_LIST_Q
    else:
        title_list = data_manager.TITLE_LIST_A
    for row in data:
        if row[0] == int(type_id) and direction == "up":
            if type == 'question':
                row[3] += 1
            else:
                row[2] += 1
        elif row[0] == int(type_id) and direction == "down":
            if type == 'question':
                row[3] -= 1
            else:
                row[2] -= 1
    data_manager.save_into_file(data, title_list, f'{type}.csv')


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
def delete_from_db(cursor, id, table):
    cursor.execute(""" DELETE FROM %(table)s WHERE id = %(id)s;
                        """, {'id': id,
                              'table': table})
    return None
