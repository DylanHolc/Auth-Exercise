from flask import Flask, redirect, render_template, flash, session, request
from models import db, connect_db, User, Feedback
from forms import AddUserForm, LoginUserForm, AddFeedbackForm
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///auth_exercise"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'Chizzle'

connect_db(app)
with app.app_context():
    db.create_all()

@app.route('/')
def register():
    return redirect('/register')

@app.route('/register', methods = ['GET', 'POST'])
def show_register():
    form = AddUserForm()
    if form.validate_on_submit():
        username = form.username.data 
        password = form.password.data 
        email = form.email.data
        first_name = form.first_name.data 
        last_name = form.last_name.data
        new_user = User.register(username, password, email, first_name, last_name)
        session['username'] = new_user.username
        db.session.add(new_user)
        db.session.commit()
        return redirect(f'/users/{username}')

    return render_template('register.html', form = form)

@app.route('/users/<username>')
def show_user(username):
    user = User.query.filter_by(username = username).first_or_404()
    all_feedback = Feedback.query.filter_by(username = username).all()
    if 'username' not in session:
        flash('You must be logged in to access!')
        return redirect('/login')
    
    else:
        return render_template('details.html', user = user, all_feedback = all_feedback)
        

@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginUserForm()
    if form.validate_on_submit():
        username = form.username.data
        password =form.password.data
        
        user = User.authenticate(username, password)
        if user:
            flash(f'Greetings {user.username}!')
            session['username'] = user.username
            return redirect(f'/users/{username}')
        else:
            form.username.errors = ['Invalid Username/Password.']

    
    return render_template('login.html', form = form)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/users/<username>/delete', methods = ['POST'])
def delete_user(username):
    if 'username' not in session:
        flash('You must be logged in to access!')
        return redirect('/login')
    user = User.query.get(username)
    all_feedback = Feedback.query.filter_by(username = username).all()
    if user.username == session['username']:
        for feedback in all_feedback:
            db.session.delete(feedback)
            db.session.commit()
        db.session.delete(user)
        db.session.commit()
        session.clear()
        return redirect('/login')

@app.route('/users/<username>/feedback/add', methods = ['GET', 'POST'])
def add_feedback(username):
    if 'username' not in session:
        flash('You must be logged in to access!')
        return redirect('/login')
    form = AddFeedbackForm()
    user = User.query.filter_by(username = username).first_or_404()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        username = session['username']
        new_feedback = Feedback(title = title, content = content, username = username)
        db.session.add(new_feedback)
        db.session.commit()
        return redirect(f'/users/{username}')
    
    return render_template('feedback_form.html', form = form, user = user)

@app.route('/feedback/<feedback_id>/update')
def show_edit_form(feedback_id):
    feedback = Feedback.query.get_or_404(feedback_id)
    username = session['username']
    if feedback.username != session['username']:
        flash('Must be logged in as author to edit!')
        return redirect(f'/users/{username}')
    else:
        return render_template('edit_feedback.html', feedback = feedback)

@app.route('/feedback/<feedback_id>/update', methods = ["POST"])
def edit_feedback(feedback_id):
    username = session['username']
    feedback = Feedback.query.get_or_404(feedback_id)
    feedback.title = request.form['title']
    feedback.content = request.form['content']
    db.session.add(feedback)
    db.session.commit()
    return redirect(f'/users/{username}')