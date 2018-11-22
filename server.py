from flask import Flask, render_template, request, redirect, url_for
import csv
import time
import data_manager
import operator
import connection
import util


app = Flask(__name__)


@app.route('/<type>/<int:type_id>/vote/<int:question_id>/<direction>')
def vote(type, type_id, direction, question_id):
    change_vote(type, direction, type_id)
    return redirect(f"/question/{question_id}")


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


@app.route('/')
@app.route('/list')
def route_list():
    sort_options = ['ID', 'Submitted', 'Views', 'Rating', 'Title']
    orderby = ['Ascending','Descending']

    status = request.args.get('status', default=0, type=int)
    order = request.args.get('order', default=0, type=int)
    questions = data_manager.get_all_data('question.csv')
    for question in questions:
        question[1] = time.strftime('%Y-%m-%d %H:%M', time.localtime(int(question[1])))
    if 'status':
        if order:
            questions = sorted(questions, key=operator.itemgetter(status), reverse=True)
        else:
            questions = sorted(questions, key=operator.itemgetter(status))
    return render_template('list.html', questions = questions, sort_options = sort_options,current=status,corder=order,orderby=orderby)


@app.route('/delete',methods=['post'])
def delete_question():
    id=request.form['questid']
    questions= data_manager.get_all_data('question.csv')
    for question in questions:
        if question[0]==int(id):
            questions.remove(question)
    data_manager.save_into_file(questions, data_manager.TITLE_LIST_Q, 'question.csv')
    answers = data_manager.get_all_data('answer.csv')
    for i in range(len(answers)):
        if i<len(answers) and int(answers[i][3]) == int(id) :
            answers[i]=""
            i-=1
    data_manager.save_into_file(answers, data_manager.TITLE_LIST_A, 'answer.csv')
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
    data_manager.save_into_file(answers, data_manager.TITLE_LIST_A, 'answer.csv')
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
    data_manager.save_into_file(questions, data_manager.TITLE_LIST_Q, 'question.csv')
    return render_template('question.html', question = returned_question, answers = filtered_answers)


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


@app.route('/ask_question', methods=['GET', 'POST'])
def route_submit_question():
    if request.method == 'POST':
        print('POST request received!')
        questions = data_manager.get_all_data('question.csv')
        id_list = []
        for question in questions:
            id_list.append(int(question[0]))
        id = str(max(id_list)+1)
        data = [id, str(int(time.time())), '0', '0', request.form['title'], request.form['question'], request.form['image']]
        questions.append(data)
        data_manager.save_into_file(questions, data_manager.TITLE_LIST_Q, 'question.csv')
        return redirect(f'/question/{id}')
    else:
        return render_template('form.html')


if __name__ == '__main__':
    app.secret_key = "wWeRt56"
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=True,
    )
