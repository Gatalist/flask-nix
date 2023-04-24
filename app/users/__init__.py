from flask import Blueprint, render_template, session, request, flash, redirect, url_for, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.urls import url_parse
from flask_login import login_required, login_user, current_user, logout_user
from app import db
from app import login_manager
from .models import Users


users = Blueprint('app_users', __name__, template_folder='templates', static_folder='static')


@login_manager.user_loader
def load_user(id):
    return Users.query.get(int(id))


@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('app_movies.view_movie'))


@users.route('/register', methods=["POST", "GET"])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        pwd_1 = request.form['pwd-1']
        pwd_2 = request.form['pwd-2']

        generate_hash_1 = generate_password_hash(pwd_1)

        if len(name) < 3:
            flash("Short name", "error_name")
        elif email.find('@') == -1:
            flash("Incorrect email", "error_email")
        elif len(pwd_1) < 8:
            flash("Password must be at least 8 characters long, contain a capital letter and symbols", "error_pwd")

        elif not check_password_hash(generate_hash_1, pwd_2):
            flash("Passwords do not match", "error_pwd-2")
            # print("pasword - ok")

        else:
            try:
                user = Users(username=name, email=email, pwd=generate_hash_1)
                db.session.add(user)
                db.session.commit()
                flash("you have successfully registered")
                return redirect(url_for('app_users.login'))
            except Exception as error:
                print(error)
                flash("Save error user in DataBase", "error_save")
        
        print(name, email, pwd_1, pwd_2)

    return render_template('register.html')



@users.route('/login', methods=["POST", "GET"])
def login():
    if request.method == 'POST':
        email = request.form['email']
        pwd = request.form['pwd-1']
        remember = request.form['remember']
        print(email, pwd)

        user = Users.query.filter_by(email=email).first()

        if user is None or not check_password_hash(user.pwd, pwd):
            flash("No correct email or password", "error_save")
            return redirect(url_for('app_users.login'))
        
        login_user(user, remember=remember)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('app_movies.view_movie')

        return redirect(next_page)
    
    return render_template('login.html', form=request.form)





# @users.route('/profile', methods=["POST", "GET"])
# def profile():
    # if request.method == 'POST':
    #     email = request.form['email']
    #     pwd = request.form['pwd-1']
    #     # remember = request.form['remember']
    #     print(email, pwd)

    #     user = Users.query.filter_by(email=email).first()
    #     if user:
    #         print(user)
    #     else:
    #         print("no user")

        # check_password_hash(user.pwd, pwd)
        
        
    # session.permanent = True
    # return render_template('profile.html')



# @app.route('/user/<name>', methods=['GET', 'POST'])
# @login_required
# def user(name):
#     user_id = current_user.id
#     user = User.query.filter(User.id==user_id).first()
#     movies = Movie.query.filter(Movie.user_id==user_id).all()
#     return render_template('user.html', user=user, movies=movies)