from flask import Flask, render_template, request, redirect, session, url_for
import csv
import time
import data_manager
import operator
import connection
import util

# (sorted(l, key=operator.itemgetter(1))) - l = list, 1 = index to sort by

app = Flask(__name__)


@app.route('/')
@app.route('/list', methods=['GET', 'POST'])
def route_list():
    questions = data_manager.get_all_data('question.csv')
    try:
        session['status'] = int(request.form.get('status'))
    except:
        pass
    if 'status' in session:
        questions = sorted(questions, key=operator.itemgetter(session['status']))
    for question in questions:
        question[1] = time.strftime('%Y-%m-%d %H:%M', time.localtime(int(question[1])))
    return render_template('list.html', questions = reversed(questions))


@app.route('/delete',methods=['post'])
def delete_question():
    id=request.form['questid']
    questions= data_manager.get_all_data('question.csv')
    for question in questions:
        if int(question[0])==int(id):
            questions.remove(question)
    questions.insert(0, data_manager.TITLE_LIST_Q)
    data_manager.save_into_file(questions,'question.csv')
    answers = data_manager.get_all_data('answer.csv')
    for i in range(len(answers)):
        if i<len(answers) and int(answers[i][3]) == int(id) :
            answers[i]=""
            i-=1
    answers.insert(0, data_manager.TITLE_LIST_A)
    data_manager.save_into_file(answers,'answer.csv')
    return redirect('/')


@app.route('/delete_answer', methods=['post'])
def delete_answer():
    id = request.form['answer_id']
    answers = data_manager.get_all_data('answer.csv')
    qid = 0
    for answer in answers:
        if answer[0] == int(id):
            qid = answer[3]
            answers.remove(answer)
    answers.insert(0, data_manager.TITLE_LIST_A)
    data_manager.save_into_file(answers, 'answer.csv')
    return redirect(f"/question/{qid}")


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
    return redirect(f'/question/{id}')


if __name__ == '__main__':
    app.secret_key = "wWeRt56"
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=True,
    )
