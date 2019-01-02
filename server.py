from flask import Flask, render_template, request, redirect, url_for, session, escape
import data_manager
import connection


app = Flask(__name__)


@app.route('/', defaults={'error': None})
@app.route('/list', defaults={'error': None})
@app.route('/list/<error>')
def route_list(error):
    style = data_manager.get_style()
    status = request.args.get('status', default=0, type=int)
    order = request.args.get('order', default=0, type=int)
    if request.path == "/list":
        order_direction, questions, sort_options = data_manager.get_question_list(0)
    else:
        order_direction, questions, sort_options = data_manager.get_question_list(1)
    return render_template('list.html', questions=questions, sort_options=sort_options, orderby=order_direction,
                           current=status, corder=order, style=style, error = error, username = session.get('username'))


@app.route('/test')
def testlogin():
    if 'username' in session:
        return 'Logged in as %s' % escape(session['username'])
    return 'nope'


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
        user_id = connection.get_user_by_name(session.get('username'))
        question = connection.add_question(title, message, image, user_id)
        return redirect(url_for('route_question', qid=question['id']))
    else:
        return render_template('form.html', style=connection.get_style())


@app.route('/edit/<int:qid>', methods=['post'])
@app.route('/question/<int:qid>', methods=['post'])
@app.route('/question/<int:qid>')
def route_question(qid):
    editable = data_manager.check_for_edit_or_save(qid)
    questions = connection.get_all_questions('id', "", 0)
    returned_question = data_manager.get_question_to_show(qid, questions)
    user = connection.get_user(returned_question.get('user_id'))
    connection.update_view_number(qid)
    return render_template('question.html', question=returned_question, editable=editable,
                           style=connection.get_style(), user_name=user['username'])


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
    user_id = connection.get_user_by_name(session.get('username'))
    connection.add_answer(qid, answer_text, user_id)
    return redirect(f"/question/{qid}")


@app.route('/comment/<type>/<qid>', methods=['POST'])
def add_comment(type, qid):
    if type == 'question':
        comment_text = request.form["commenttext"]
        user_id = connection.get_user_by_name(session.get('username'))
        connection.add_comment('question_id', qid, comment_text, user_id)
    elif type == 'answer':
        comment_text = request.form["commenttext"]
        user_id = connection.get_user_by_name(session.get('username'))
        connection.add_comment('answer_id', qid, comment_text, user_id)
        qid = request.form['question_id']
    return redirect(f"/question/{qid}")


@app.route('/search')
def search():
    sort_options = ['ID', 'Submitted', 'Views', 'Rating', 'Title']
    orderby = ['Ascending', 'Descending']
    searchvalue = '%' + request.args['searchval'] + '%'
    questions = connection.get_all_questions('id', searchvalue, 0)
    return render_template('list.html', questions=questions, sort_options=sort_options, orderby=orderby, style=connection.get_style())


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        print('POST request received!')
        username = request.form['username']
        password = data_manager.hash_password(request.form['password'])
        profile_picture = request.form.get('profile_picture')
        try:
            connection.register_user(username, password, profile_picture)
        except:
            pass
        return redirect(url_for('route_list'))
    else:
        return render_template('register.html', style=connection.get_style())



@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        print('POST request received!')
        username = request.form['username']
        password_input = request.form['password']
        try:
            user_pw = connection.get_user_password(username).get('password')
        except AttributeError:
            return redirect(url_for('route_list'))
        if data_manager.verify_password(password_input, user_pw):
            session['username'] = username
            return redirect(url_for('route_list'))
        else:
            return redirect("/list/error")


@app.route('/users')
def all_users():
    users = connection.get_all_users()
    return render_template('users.html', users = users, style=connection.get_style())


@app.route('/user/<int:uid>')
def show_user_profile(uid):
    userdata = connection.get_user(uid)
    question_data = connection.get_questions_by_user(uid)
    answer_data = connection.get_answers_by_user(uid)
    comment_data = connection.get_comments_by_user(uid)
    return render_template('profile.html', userdata=userdata, questions = question_data, answers = answer_data,
                           comments = comment_data, style=connection.get_style())

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('route_list'))


if __name__ == '__main__':
    app.secret_key = "wWeRt56"
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=True,
    )
