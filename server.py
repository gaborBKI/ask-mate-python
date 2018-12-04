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
    questions = connection.get_all_questions()
    return render_template('list.html', questions=questions, sort_options=sort_options, orderby=orderby)


@app.route('/ask_question', methods=['GET', 'POST'])
def route_submit_question():
    if request.method == 'POST':
        print('POST request received!')
        title = request.form['title']
        message = request.form['question']
        image = request.form['image']
        question = connection.add_question(title, message, image)
        question_id = data_manager.get_latest_id(question)
        return redirect(f"/question/{question_id}")
    else:
        return render_template('form.html')


@app.route('/question/<int:qid>')
def route_question(qid):
    questions = connection.get_all_questions()
    answers = connection.get_all_answers()
    returned_question = data_manager.get_question_to_show(qid, questions)
    filtered_answers = data_manager.get_answers_to_question(answers, qid)
    return render_template('question.html', question=returned_question, answers=filtered_answers)


@app.route('/delete', methods=['post'])
def delete_question():
    id = request.form['questid']
    connection.delete_question_answers(id)

    connection.delete_from_db(id, 'question')
    return redirect('/')


@app.route('/delete_answer', methods=['post'])
def delete_answer():
    id = request.form['answer_id']
    connection.delete_from_db(id, 'answer')
    return redirect(f"/question/{qid}")


@app.route('/answer/<qid>', methods=['POST'])
def answer(qid):
    answer_text = request.form["answertext"]
    connection.add_answer(qid, answer_text)
    return redirect(f"/question/{qid}")


if __name__ == '__main__':
    app.secret_key = "wWeRt56"
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=True,
    )
