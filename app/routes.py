from flask import flash, redirect, render_template, session, url_for,flash
from flask_login import current_user,login_user,logout_user,login_required
from .models import *
import time
from socket import SocketIO
from .forms import LoginForm, RegisterForm
from flask import current_app as app
from . import socketio
from flask_socketio import SocketIO, join_room, leave_room, send




#defnitions
website_name = "name-here"
landing_page_text = "How are you feeling today?"

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title="Homepage - myyHealth",name = website_name,text_data = landing_page_text)

@app.route('/signup',methods = ['GET', 'POST'])
def signup():
    form = RegisterForm()
    print('\n\nDone22\n\n')
    if current_user.is_authenticated:
        print('\n\nDone77\n\n')
        return redirect(url_for('index'))
    if form.validate_on_submit():
        
        user_exist = User.query.filter_by(email=form.email.data).first()
        if user_exist is None:
            user = User(
                full_name = form.fullname.data,
                email = form.email.data,
                username = form.email.data
                )

            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            login_user(user)
            return redirect(url_for('dashboard'))
            # return "SUCCESS"
        flash('User with the same email exist')
    return render_template('signup.html', title='SignIn - goFarm', form=form)

@app.route('/signin', methods = ['GET', 'POST'])
def signin():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        print(user)
        if user is None or not user.check_password(form.password.data):
            flash('Invalid email or password')
            return redirect(url_for('signin'))
        login_user(user, remember=form.remember_me.data)
        print(current_user.is_authenticated)
        return redirect(url_for('dashboard'))
        # return "SUCCESS"
    return render_template('signin.html',form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

# @app.route('/dashboard')
# def dashboard():
#     return render_template('dashboard.html')

@app.route('/blog')
def blog():
        return render_template('blog.html')

@app.route('/stories')
def stories():
        return render_template('stories.html')

@app.route('/dashboard')
def dashboard():
    if current_user.is_authenticated:
        return render_template('dashboard.html')
    return redirect(url_for('signin'))

@app.route('/writestory')
def storymofo():
    if current_user.is_authenticated:
        return render_template('write.html')
    return redirect(url_for('signin'))



###########################
###########################
###########################
ROOMS = ["lounge", "news", "games", "coding"]

@app.route("/chat", methods=['GET', 'POST'])
def chat():

    if not current_user.is_authenticated:
        flash('Please login', 'danger')
        return redirect(url_for('signin'))

    return render_template("chat.html", username=current_user.username, rooms=ROOMS)

@socketio.on('incoming-msg')
def on_message(data):
    """Broadcast messages"""

    msg = data["msg"]
    username = data["username"]
    room = data["room"]
    # Set timestamp
    time_stamp = time.strftime('%b-%d %I:%M%p', time.localtime())
    send({"username": username, "msg": msg, "time_stamp": time_stamp}, room=room)


@socketio.on('join')
def on_join(data):
    """User joins a room"""

    username = data["username"]
    room = data["room"]
    join_room(room)

    # Broadcast that new user has joined
    send({"msg": username + " has joined the " + room + " room."}, room=room)


@socketio.on('leave')
def on_leave(data):
    """User leaves a room"""

    username = data['username']
    room = data['room']
    leave_room(room)
    send({"msg": username + " has left the room"}, room=room)

###########################
###########################
###########################

# @app.route('/dashboard')
# @login_required
# def dashboard():
#     user = current_user.uid
#     # return render_template('dashboard.html', title='Dashboard')
#     return render_template('/dashboard/dashboard.html',title='Dashboard - goFarm',uid = user)

# @app.route('/user/<id>')
# @login_required
# def user(id):
#     print(current_user.uid,":",id)
#     print(type(current_user.uid))
#     print(type(id))
#     if (str(current_user.uid) != id):
#         return redirect(url_for('unauth'))
#     else:
#         temp = User.query.filter_by(uid=id).first()
#     # if temp is None:
#     #     return render_template('notfound.html')
#         return render_template('/user/user.html',data = temp,title='Dashboard - goFarm')

# @app.route('/logo')
# def logo():
#     # return render_template('dashboard.html', title='Dashboard')
#     return render_template('/new/logo.html'  )

# @app.errorhandler(404)
# def not_found(e):
#     return render_template("404.html", title = "Oops, Page not found!")

# @app.route('/unauthorized')
# def unauth():
#     return render_template("unauth.html",title="No Permission")