from flask import Flask, render_template, request, redirect
import data_manager
import connection

app = Flask(__name__)


@app.route('/')
@app.route('/list')
def route_list():
    sort_options = ['ID', 'Submitted', 'Views', 'Rating', 'Title']
<<<<<<< HEAD
    order_direction = ['Ascending', 'Descending']
    order = data_manager.get_order_by_what(sort_options)
    direction = data_manager.get_order_direction(order_direction)
    if direction == 'DESC':
        questions = connection.get_all_questions_desc(order)
    else:
        questions = connection.get_all_questions(order)
    return render_template('list.html', questions=questions, sort_options=sort_options, orderby=order_direction)
=======
    orderby = ['Ascending', 'Descending']
    questions = connection.get_all_questions('id', "")
    return render_template('list.html', questions=questions, sort_options=sort_options, orderby=orderby)
>>>>>>> 44121e71d03e1b9c08566cae8fde3a974c676e3c


@app.route('/<type>/<int:type_id>/vote/<int:question_id>/<direction>')
def vote(type, type_id, direction, question_id):
    connection.change_vote(type, direction, type_id)
    return redirect(f"/question/{question_id}")


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


@app.route('/edit/<int:qid>', methods=['post'])
@app.route('/question/<int:qid>', methods=['post'])
@app.route('/question/<int:qid>')
def route_question(qid):
    if request.form.get('edit'):
        editable = True
    else:
        editable = False
    if request.form.get('save'):
        connection.update_question_text(qid, request.form['updated'])
    questions = connection.get_all_questions('id', "")
    answers = connection.get_all_answers()
    returned_question = data_manager.get_question_to_show(qid, questions)
    filtered_answers = data_manager.get_answers_to_question(answers, qid)
    connection.update_view_number(qid)
    return render_template('question.html', question=returned_question, answers=filtered_answers, editable=editable)

#TODO editing form box is abismal, needs fixed.

@app.route('/delete', methods=['post'])
def delete_question():
    id = request.form['questid']

    connection.delete_from_db(id, 'question', 'id')
    return redirect('/')


@app.route('/delete_answer', methods=['post'])
def delete_answer():
    qid = request.form['question_id']
    id = request.form['answer_id']
    connection.delete_from_db(id, 'answer', 'id')
    return redirect(f"/question/{qid}")


@app.route('/answer/<qid>', methods=['POST'])
def answer(qid):
    answer_text = request.form["answertext"]
    connection.add_answer(qid, answer_text)
    return redirect(f"/question/{qid}")


@app.route('/search')
def search():
    sort_options = ['ID', 'Submitted', 'Views', 'Rating', 'Title']
    orderby = ['Ascending', 'Descending']
    searchvalue = '%' + request.args['searchval'] + '%'
    questions = connection.get_all_questions('id', searchvalue)
    return render_template('list.html', questions=questions, sort_options=sort_options, orderby=orderby)



if __name__ == '__main__':
    app.secret_key = "wWeRt56"
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=True,
    )
