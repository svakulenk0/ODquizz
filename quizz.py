from datetime import datetime
# import json

from flask import Flask, request, url_for, redirect, g, session, flash, \
     abort, render_template, json
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.oauth import OAuth

from parse_table import csvclean_service

from settings import CONSUMER_KEY, CONSUMER_SECRET

table_url = None

app = Flask(__name__)
app.config.update(
    DEBUG=True,
    SQLALCHEMY_DATABASE_URI='sqlite:///odquizz.db',
    SECRET_KEY='development-key'
)
db = SQLAlchemy(app)
oauth = OAuth()

facebook = oauth.remote_app('facebook',
    base_url='https://graph.facebook.com/',
    request_token_url=None,
    access_token_url='/oauth/access_token',
    authorize_url='https://www.facebook.com/dialog/oauth',
    consumer_key=CONSUMER_KEY,
    consumer_secret=CONSUMER_SECRET,
    request_token_params={'scope': 'email'}
)


# table with many-to-many relationships for quizzes and questions
# following http://flask-sqlalchemy.pocoo.org/2.1/models/
# and https://techarena51.com/blog/many-to-many-relationships-with-flask-sqlalchemy/
quizz_questions = db.Table('quizz_questions',
                           db.Column('quizz_id', db.Integer, db.ForeignKey('quizz.id'), nullable=False),
                           db.Column('question_id', db.Integer, db.ForeignKey('question.id'), nullable=False),
                           db.PrimaryKeyConstraint('quizz_id', 'question_id'))


class Quizz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)
    pub_date = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    questions = db.relationship('Question', secondary=quizz_questions,
                                backref=db.backref('quizzes', lazy='dynamic'))

    def __init__(self, user, title):
        self.user = user
        self.title = title
        self.pub_date = datetime.utcnow()
        print "new Quizz object created"


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.Text)
    answer = db.Column(db.Text)
    table = db.Column(db.Text)
    column = db.Column(db.Integer)
    row = db.Column(db.Integer)
    pub_date = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, user, question, answer, row, column, table):
        self.user = user
        self.question = question
        self.answer = answer
        self.table = table
        self.row = row
        self.column = column
        self.pub_date = datetime.utcnow()
        print "new question object created"


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    display_name = db.Column(db.String(120))
    fb_id = db.Column(db.String(30), unique=True)
    questions = db.relationship(Question, lazy='dynamic', backref='user')


@app.before_request
def check_user_status():
    g.user = None
    if 'user_id' in session:
        g.user = User.query.get(session['user_id'])


def generate_table(table_url):
    table = csvclean_service(table_url)
    # run with default csv url
    # table = csvclean_service()
    header = json.dumps(table.header_line)
    rows = json.dumps(table.sample[1:])
    return (header, rows)


@app.route('/', methods=['GET', 'POST'])
def new_question():
    global table_url
    rows = None
    header = None
    if request.method == 'POST':
        # return render_template('table.html', rows=rows, header=header)
        # if 'url' in request.form:
            # print request.form['url']
        table_url = request.form['url']
        header, rows = generate_table(table_url)
        # elif 'question' in request.form:
        #     print request.form['question']
        #     string = request.form['question']
        #     row = request.form['row']
        #     column = request.form['col']
        #     question_obj = Question(g.user, string, row, column, table_url)
        #     db.session.add(question_obj)
        #     db.session.commit()
            # return redirect(url_for('show_question', question_id=question_obj.id))
    return render_template('new_question.html', rows=rows, header=header)


@app.route('/new_question', methods=['GET', 'POST'])
def add_question():
    global table_url
    if request.method == 'POST':
        question = request.form['question']
        row = request.form['row']
        column = request.form['col']
        answer = request.form['answer']
        question_obj = Question(g.user, question, answer, row, column, table_url)
        db.session.add(question_obj)
        db.session.commit()
        return redirect(url_for('show_question', question_id=question_obj.id))
    return render_template('layout.html')


@app.route('/<int:question_id>')
def show_question(question_id):
    print "im showing the question:"
    question_obj = Question.query.get_or_404(question_id)
    print question_obj.question
    header, rows = generate_table(question_obj.table)
    return render_template('show_question.html', question_obj=question_obj,
                            header=header, rows=rows)


@app.route('/<int:question_id>/delete', methods=['GET', 'POST'])
def delete_question(question_id):
    question_obj = Question.query.get_or_404(question_id)
    if g.user is None or g.user != question_obj.user:
        abort(401)
    if request.method == 'POST':
        if 'yes' in request.form:
            db.session.delete(question_obj)
            db.session.commit()
            flash('Question was deleted')
            return redirect(url_for('new_question'))
        else:
            return redirect(url_for('show_question', question_id=question_obj.id))
    return render_template('delete_question.html', question_obj=question_obj)


@app.route('/quizz', methods=['GET', 'POST'])
def new_quizz():
    rows = None
    header = None
    print request.form
    if 'question' in request.form:
        question_obj = request.form['question']
        print question_obj.question
        header, rows = generate_table(question_obj.table)
        return render_template('show_quizz.html', quizz_obj=quizz_obj,
                                header=header, rows=rows)
    question_ids = request.form.getlist('questions')
    # store quiz in DB
    quizz_obj = Quizz(g.user, title="Local Ignorance Test")
    db.session.add(quizz_obj)
    # add all questions to the quizz
    for question_id in question_ids:
        question_obj = Question.query.get(question_id)
        if question_obj is not None:
            quizz_obj.questions.append(question_obj)
    db.session.commit()
    return render_template('show_quizz.html', quizz_obj=quizz_obj,
                            header=header, rows=rows)


@app.route('/my-questions', methods=['GET', 'POST'])
def my_questions():
    # if g.user is None:
    #     return redirect(url_for('login', next=request.url))
    question_objs = Question.query.filter_by(user=g.user).all()
    return render_template('my_questions.html', question_objs=question_objs)


@app.route('/delete-my-questions', methods=['GET', 'POST'])
def delete_my_questions():
    if g.user is None:
        return redirect(url_for('login', next=request.url))
    if request.method == 'POST':
        if 'yes' in request.form:
            # for question_obj in ques
            question_objs = Question.query.filter_by(user=g.user).delete()
            # db.session.de.delete(question_objs)
            db.session.commit()
            flash('Questions were deleted')
            return redirect(url_for('new_question'))
        else:
            return redirect(url_for('show_question', question_id=question_obj.id))
    return render_template('delete_questions.html')



@app.route('/login')
def login():
    return facebook.authorize(callback=url_for('facebook_authorized',
        next=request.args.get('next') or request.referrer or None,
        _external=True))


@app.route('/logout')
def logout():
    session.clear()
    flash('You were logged out')
    return redirect(url_for('new_question'))


@app.route('/login/authorized')
@facebook.authorized_handler
def facebook_authorized(resp):
    next_url = request.args.get('next') or url_for('new_question')
    if resp is None:
        flash('You denied the login')
        return redirect(next_url)

    session['fb_access_token'] = (resp['access_token'], '')

    me = facebook.get('/me')
    user = User.query.filter_by(fb_id=me.data['id']).first()
    if user is None:
        user = User()
        user.fb_id = me.data['id']
        db.session.add(user)

    user.display_name = me.data['name']
    db.session.commit()
    session['user_id'] = user.id

    flash('You are now logged in as %s' % user.display_name)
    return redirect(next_url)


@facebook.tokengetter
def get_facebook_oauth_token():
    return session.get('fb_access_token')


if __name__ == '__main__':
    app.run(port=5001)
