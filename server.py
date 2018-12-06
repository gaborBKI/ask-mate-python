from flask import Flask, render_template, request, redirect
import data_manager
import connection

app = Flask(__name__)


#TODO make sure check_for_edit_or_save and get_question_list functions are moved to data_manager
#TODO add corder and order back so the html order menus remember that status


@app.route('/')
@app.route('/list')
def route_list():
    status = request.args.get('status', default=0, type=int)
    order = request.args.get('order', default=0, type=int)
    if request.path == "/list":
        order_direction, questions, sort_options = data_manager.get_question_list(0)
    else:
        order_direction, questions, sort_options = data_manager.get_question_list(1)

    return render_template('list.html', questions=questions, sort_options=sort_options, orderby=order_direction, current=status, corder=order)


@app.route('/<type>/<int:type_id>/vote/<int:question_id>/<direction>')
def vote(type, type_id, direction, question_id):
    data_manager.change_vote(type, direction, type_id)
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
    editable = data_manager.check_for_edit_or_save(qid)
    questions = connection.get_all_questions('id', "", 0)
    answers = connection.get_all_answers()
    returned_question = data_manager.get_question_to_show(qid, questions)
    filtered_answers = data_manager.get_answers_to_question(answers, qid)
    question_comments = connection.get_all_comments('question', qid)
    answer_comments = connection.get_all_comments('answer', qid)
    connection.update_view_number(qid)
    return render_template('question.html', question=returned_question, answers=filtered_answers, editable=editable,
                           question_comments = question_comments, answer_comments = answer_comments)


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
    questions = connection.get_all_questions('id', searchvalue, 0)
    return render_template('list.html', questions=questions, sort_options=sort_options, orderby=orderby)


if __name__ == '__main__':
    app.secret_key = "wWeRt56"
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=True,
    )
