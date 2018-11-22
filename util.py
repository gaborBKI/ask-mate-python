import time


def convert_time(data, row):
    data[row] = time.strftime('%Y-%m-%d %H:%M', time.localtime(int(data[row])))


def generate_id_for_question(questions):
    id_list = []
    for question in questions:
        id_list.append(int(question[0]))
    id = str(max(id_list) + 1)
    return id


def get_question_by_id(qid, questions):
    returned_question = []
    for question in questions:
        if qid == int(question[0]):
            question[2] = str(int(question[2]) + 1)
            returned_question = question[:]
            convert_time(returned_question, 1)
    return returned_question


def get_answer_by_id(answers, qid):
    filtered_answers = []
    for answer in answers:
        answer[1] = time.strftime('%Y-%m-%d %H:%M', time.localtime(int(answer[1])))
        if qid == int(answer[3]):
            filtered_answers.append(answer)
    return filtered_answers


def remove_question_by_id(id, questions):
    for question in questions:
        if question[0] == int(id):
            questions.remove(question)


def remove_answer_by_id(answers, id):
    for answer in answers:
        if answer[0] == int(id):
            qid = answer[3]
            answers.remove(answer)


def remove_answers_to_deleted_question(answers, id):
    for i in range(len(answers)):
        if i < len(answers) and int(answers[i][3]) == int(id):
            answers[i] = ""
            i -= 1