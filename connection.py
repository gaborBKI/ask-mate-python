import data_manager
import operator
import time
import database_common


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
