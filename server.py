from flask import Flask, render_template, request, redirect, url_for
import csv
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
            question[2] = str(int(question[2]) + 1)
            returned_question = question[:]
            returned_question[1] = time.strftime('%Y-%m-%d %H:%M', time.localtime(int(returned_question[1])))
    for answer in answers:
        answer[1] = time.strftime('%Y-%m-%d %H:%M', time.localtime(int(answer[1])))
        if qid == int(answer[3]):
            filtered_answers.append(answer)
    questions.insert(0, data_manager.TITLE_LIST_Q)
    data_manager.save_into_file(questions, 'question.csv')
    return render_template('question.html', question = returned_question, answers = filtered_answers)


@app.route('/ask_question', methods=['GET'])
def rout_ask_question():
    return render_template('form.html')


@app.route('/answer/<qid>', methods=['POST'])
def answer(qid):
    answers=data_manager.get_all_data("answer.csv")
    id_list = []
    for answer in answers:
        id_list.append(int(answer[0]))
    id = str(max(id_list) + 1)
    with open("answer.csv","a") as file:
        writer = csv.writer(file)
        writer.writerow([id,int(time.time()),0,qid,request.form["answertext"]])
    return redirect(f"/question/{qid}")


@app.route('/ask_question', methods=['POST'])
def route_submit_question():
    print('POST request received!')
    questions = data_manager.get_all_data('question.csv')
    id_list = []
    for question in questions:
        id_list.append(int(question[0]))
    id = str(max(id_list)+1)
    data = [id, str(int(time.time())), '0', '0', request.form['title'], request.form['question'], request.form['image']]
    questions.insert(0, data_manager.TITLE_LIST_Q)
    questions.append(data)
    data_manager.save_into_file(questions, 'question.csv')
    return redirect('/')


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=True,
    )
