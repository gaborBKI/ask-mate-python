from flask import request
import connection
import bcrypt


def get_latest_id(question):
    question_id = 0
    for data in question:
        question_id += data['id']
    return question_id


def get_answers_to_question(answers, qid):
    filtered_answers = []
    for answer in answers:
        if answer['question_id'] == qid:
            filtered_answers.append(answer)

            answer["comments"] = connection.get_all_comments('answer', answer['id'])
    return filtered_answers


def get_question_to_show(qid, questions):
    for question in questions:
        if question['id'] == qid:
            returned_question = question
    return returned_question


def get_order_by_what(sort_options):
    sort_by = {'ID': 'id', 'Submitted': 'submission_time', 'Views': 'view_number', 'Rating': 'vote_number',
               'Title': 'title'}
    sort_by_what = request.args.get('status', default=0, type=int)
    sort_method = sort_options[sort_by_what]
    sorting = sort_by[sort_method]
    return sorting


def get_order_direction(order_direction):
    direction = {'Ascending': 'ASC', 'Descending': 'DESC'}
    the_way = request.args.get('order', default=0, type=int)
    way_method = order_direction[the_way]
    sorting_direction = direction[way_method]
    return sorting_direction


def change_vote(type, direction, type_id):
    questions = connection.get_all_questions('id', '', 0)
    answers = connection.get_all_answers()
    if type == 'question':
        for question in questions:
            if question['id'] == int(type_id) and direction == "up":
                connection.update_vote(type, 1, type_id)
            elif question['id'] == int(type_id) and direction == "down":
                connection.update_vote(type, -1, type_id)
    elif type == 'answer':
        for answer in answers:
            if answer['id'] == int(type_id) and direction == "up":
                connection.update_vote(type, 1, type_id)
            elif answer['id'] == int(type_id) and direction == "down":
                connection.update_vote(type, -1, type_id)


def get_order_by_user(order, questions, status):
    if 'status':
        if order:
            questions = sorted(questions, key=operator.itemgetter(status), reverse=True)
        else:
            questions = sorted(questions, key=operator.itemgetter(status))
    return questions


def get_question_list(limit):
    sort_options = ['ID', 'Submitted', 'Views', 'Rating', 'Title']
    order_direction = ['Ascending', 'Descending']
    if not limit:
        order = get_order_by_what(sort_options)
        direction = get_order_direction(order_direction)
        if direction == 'DESC':
            questions = connection.get_all_questions_desc(order)
        elif direction == 'ASC':
            questions = connection.get_all_questions_asc(order)
    else:
        questions = connection.get_all_questions('submission_time', "", True)
    return order_direction, questions, sort_options


def check_for_edit_or_save(qid):
    if request.form.get('edit'):
        editable = True
    else:
        editable = False
    if request.form.get('save'):
        connection.update_question_text(qid, request.form['updated'])
    return editable


def get_style():
    if request.args.get('style'):
        colour = request.args['style']
        style = connection.make_style(colour)
    else:
        style = connection.get_style()
    return style


def hash_password(plain_text_password):
    hashed_bytes = bcrypt.hashpw(plain_text_password.encode('utf-8'), bcrypt.gensalt())
    return hashed_bytes.decode('utf-8')


def verify_password(plain_text_password, hashed_password):
    hashed_bytes_password = hashed_password.encode('utf-8')
    return bcrypt.checkpw(plain_text_password.encode('utf-8'), hashed_bytes_password)
