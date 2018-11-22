from flask import Flask, render_template, request, redirect
import time
import data_manager
import connection
import util

app = Flask(__name__)


@app.route('/<type>/<int:type_id>/vote/<int:question_id>/<direction>')
def vote(type, type_id, direction, question_id):
    connection.change_vote(type, direction, type_id)
    return redirect(f"/question/{question_id}")


@app.route('/')
@app.route('/list')
def route_list():
    sort_options = ['ID', 'Submitted', 'Views', 'Rating', 'Title']
    orderby = ['Ascending', 'Descending']
    questions = data_manager.get_all_data('question.csv')
    for question in questions:
        util.convert_time(question, 1)
    status = request.args.get('status', default=0, type=int)
    order = request.args.get('order', default=0, type=int)
    questions = connection.get_order_by_user(order, questions, status)
    return render_template('list.html', questions=questions, sort_options=sort_options, current=status, corder=order,
                           orderby=orderby)


@app.route('/delete', methods=['post'])
def delete_question():
    id = request.form['questid']
    questions = data_manager.get_all_data('question.csv')
    util.remove_question_by_id(id, questions)
    data_manager.save_into_file(questions, data_manager.TITLE_LIST_Q, 'question.csv')
    answers = data_manager.get_all_data('answer.csv')
    util.remove_answers_to_deleted_question(answers, id)
    data_manager.save_into_file(answers, data_manager.TITLE_LIST_A, 'answer.csv')
    return redirect('/')


@app.route('/delete_answer', methods=['post'])
def delete_answer():
    id = request.form['answer_id']
    answers = data_manager.get_all_data('answer.csv')
    qid = util.remove_answer_by_id(answers, id)
    data_manager.save_into_file(answers, data_manager.TITLE_LIST_A, 'answer.csv')
    return redirect(f"/question/{qid}")


@app.route('/question/<int:qid>')
def route_question(qid):
    questions = data_manager.get_all_data('question.csv')
    answers = data_manager.get_all_data('answer.csv')
    returned_question = util.get_question_by_id(qid, questions)
    filtered_answers = util.get_answer_by_id(answers, qid)
    data_manager.save_into_file(questions, data_manager.TITLE_LIST_Q, 'question.csv')
    return render_template('question.html', question=returned_question, answers=filtered_answers)


@app.route('/answer/<qid>', methods=['POST'])
def answer(qid):
    answers = data_manager.get_all_data("answer.csv")
    id_list = []
    for answer in answers:
        id_list.append(int(answer[0]))
    id = str(max(id_list) + 1)
    data_manager.append_answer_into_file(id, qid, request.form["answertext"])
    return redirect(f"/question/{qid}")


@app.route('/ask_question', methods=['GET', 'POST'])
def route_submit_question():
    if request.method == 'POST':
        print('POST request received!')
        questions = data_manager.get_all_data('question.csv')
        question_id = util.generate_id_for_question(questions)
        connection.get_question_by_user(question_id, questions, request.form['title'], request.form['question'],
                                        request.form['image'])
        return redirect(f'/question/{question_id}')
    else:
        return render_template('form.html')


if __name__ == '__main__':
    app.secret_key = "wWeRt56"
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=True,
    )
