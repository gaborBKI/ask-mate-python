import csv
import os
import time


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
    return filtered_answers


def get_question_to_show(qid, questions):
    for question in questions:
        if question['id'] == qid:
            returned_question = question
    return returned_question
