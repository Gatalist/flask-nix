from flask import Blueprint, render_template



users = Blueprint('app_users', __name__, template_folder='templates', static_folder='static')


@users.route('/', methods=["POST", "GET"])
def view_user():

    return render_template('index.html')

