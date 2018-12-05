import csv
import os
import time
from flask import request

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

def get_order_by_what(sort_options):
    sort_by = {'ID': 'id', 'Submitted': 'submission_time', 'Views': 'view_number', 'Rating': 'vote_number',
               'Title': 'title'}
    sort_by_what = request.args.get('status', default=0, type=int)
    sort_method = sort_options[sort_by_what]
    sorting = sort_by[sort_method]
    print(sorting)
    return sorting


def get_order_direction(order_direction):
    direction = {'Ascending': 'ASC', 'Descending': 'DESC'}
    the_way = request.args.get('order', default=0, type=int)
    way_method = order_direction[the_way]
    sorting_direction = direction[way_method]
    print(sorting_direction)
    return sorting_direction
