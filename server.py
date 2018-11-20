from flask import Flask, render_template, request, redirect, url_for

import time
import data_manager
import connection
import util

app = Flask(__name__)


@app.route('/')
@app.route('/list')
def route_list():
    questions = data_manager.get_all_data('question.csv')
    for question in questions:
        question[1] = time.strftime('%Y-%m-%d %H:%M', time.localtime(int(question[1])))
    return render_template('list.html', questions = questions)

@app.route('/question/<int:qid>')
def route_question(qid):
    questions = data_manager.get_all_data('question.csv')
    answers = data_manager.get_all_data('answer.csv')
    filtered_answers = []
    returned_question = []
    for question in questions:
        if qid == int(question[0]):
            returned_question = question
            returned_question[1] = time.strftime('%Y-%m-%d %H:%M', time.localtime(int(returned_question[1])))
    for answer in answers:
        if qid == int(answer[3]):
            filtered_answers.append(answer)
    return render_template('question.html', question = returned_question, answers = filtered_answers)

if __name__ == '__main__':
    app.run(
        port=8000,
        debug=True,
    )
