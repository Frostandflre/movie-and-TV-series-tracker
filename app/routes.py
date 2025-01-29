from flask import render_template, redirect,url_for,Blueprint,session,flash
from werkzeug.security import generate_password_hash, check_password_hash
from .forms import RegistrationForm,AuthorizationForm
from .extensions import database
from .models import Users

main = Blueprint('main', __name__)

@main.route("/start_page")
def start_page():
    return render_template('start_page.html')

@main.route("/")
def main_page():
    return render_template('main_page.html')

@main.route("/login",methods=['GET', 'POST'])
def login_page():
    form = AuthorizationForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = Users.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            return redirect(url_for('main.main_page'))
        else:
            flash("Неправильный email или пароль!","error")
            return redirect(url_for('main.login_page'))
    return render_template('login_page.html', form=form)

@main.route("/registration",methods=['GET', 'POST'])
def registration_page():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = Users(nickname=form.nickname.data,password=generate_password_hash(form.password.data,salt_length=128), email=form.email.data)
        database.session.add(user)
        database.session.commit()
        session['user_id'] = user.user_id
        return redirect(url_for("main.main_page"))
    return render_template("registration_page.html",form=form)
