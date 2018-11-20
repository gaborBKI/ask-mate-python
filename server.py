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
        question[1] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(question[1])))
    return render_template('list.html', questions = questions)

@app.route('/question/<int:qid>')
def route_question(qid):
    questions = data_manager.get_all_data('question.csv')
    for question in questions:
        if qid == int(question[0]):
            question[1] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(question[1])))
            return render_template('question.html', question = question)

if __name__ == '__main__':
    app.run(
        port=8000,
        debug=True,
    )
