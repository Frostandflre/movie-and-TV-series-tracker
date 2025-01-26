from flask import render_template, redirect,url_for,session,Blueprint
from .forms import RegistrationForm

main = Blueprint('main', __name__)

users = []

class User:
    def __init__(self, nickname, email,password):
        self.nickname = nickname
        self.password = None  # TODO: Добавить хэширование пароля
        self.email = email
        self.watched_movies = []
        self.watched_TV_series = []
        self.is_authenticated = False
        self.is_admin = False

@main.route("/start_page")
def start_page():
    return render_template('start_page.html')

@main.route("/")
def main_page():
    return render_template('main_page.html')

@main.route("/registration")
def registration_page():
    form = RegistrationForm()
    if form.validate_on_submit():
        return redirect(url_for("main_page"))
    return render_template("registration_page.html",form=form)
