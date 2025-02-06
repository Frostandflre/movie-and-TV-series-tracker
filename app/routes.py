from flask import render_template, redirect,url_for,Blueprint,session,flash,make_response,request,jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from .forms import RegistrationForm,AuthorizationForm
from .extensions import database
from .models import Users, MovieStatus
from .movie_logic import get_movie_info,get_popular_movies,search_movie

main = Blueprint('main', __name__)

@main.route("/")
def main_page(): # TODO: исправить проблему с маштабируемостью
    if not session.get('current_page'):
        session['current_page'] = 1
    nickname = "Guest"
    if 'nickname' in request.cookies:
        nickname = request.cookies.get('nickname')
    popular_movies = get_popular_movies(session['current_page'])
    return render_template('main_page.html',nickname=nickname,popular_movies=popular_movies,current_page=session['current_page'])

@main.route("/next_page/<redirect_to>",defaults = {'search_query': None})
@main.route("/next_page/<redirect_to>/<search_query>")
def next_page(redirect_to,search_query):
    session['current_page'] += 1
    return redirect(url_for(f"main.{redirect_to}",term=search_query))

@main.route("/previous_page/<redirect_to>",defaults = {'search_query': None})
@main.route("/previous_page/<redirect_to>/<search_query>")
def previous_page(redirect_to,search_query):
    if session['current_page'] > 1:
        session['current_page'] -= 1
    return redirect(url_for(f"main.{redirect_to}",term=search_query))

@main.route("/reset_page/<redirect_to>",defaults = {'search_query': None})
@main.route("/reset_page/<redirect_to>/<search_query>")
def reset_page(redirect_to,search_query):
    session['current_page'] = 1
    return redirect(url_for(f"main.{redirect_to}",term=search_query))

@main.route("/login",methods=['GET', 'POST'])
def login_page(): # TODO: обновить дизайн
    nickname = "Guest"
    if 'nickname' in request.cookies:
        nickname = request.cookies.get('nickname')
    form = AuthorizationForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = Users.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            nickname = user.nickname
            user_id = str(user.user_id)
            response = make_response(redirect(url_for('main.main_page')))
            response.set_cookie('nickname', nickname,max_age=60*60*24*30, secure=True, httponly=True,)
            response.set_cookie('user_id', user_id, max_age=60*60*24*30, secure=True, httponly=True, )
            return response
        else:
            flash("Неправильный email или пароль!","error")
            return redirect(url_for('main.login_page'))
    return render_template('login_page.html', form=form,nickname=nickname)

@main.route("/logout")
def logout_page():
    response = make_response(redirect(url_for('main.main_page')))
    response.set_cookie('nickname', '', expires=0)
    response.set_cookie('user_id', '', expires=0)
    return response

@main.route("/registration",methods=['GET', 'POST'])
def registration_page(): # TODO: обновить дизайн
    nickname = "Guest"
    if 'nickname' in request.cookies:
        nickname = request.cookies.get('nickname')
    form = RegistrationForm()
    if form.validate_on_submit():
        user = Users(nickname=form.nickname.data,password=generate_password_hash(form.password.data,salt_length=128), email=form.email.data)
        database.session.add(user)
        database.session.commit()
        return redirect(url_for("main.main_page"))
    return render_template("registration_page.html",form=form,nickname=nickname)

@main.route("/movie_info/<movie_id>")
def movie_info_page(movie_id):
    nickname = "Guest"
    if 'nickname' in request.cookies:
        nickname = request.cookies.get('nickname')
    user_id = request.cookies.get('user_id')
    current_status = MovieStatus.query.filter_by(user_id=user_id, movie_id=movie_id).first().status if user_id else "Не просмотрено"
    movie_info = get_movie_info(movie_id)
    return render_template("movie_info_page.html",nickname=nickname,movie_info=movie_info,movie_id=movie_id,current_status=current_status)

@main.route("/save_movie_status", methods=["POST"])
def save_movie_status():
    data = request.get_json()
    user_id = request.cookies.get('user_id')

    if not user_id:
        return jsonify({"error": "Пользователь не авторизован"}), 401

    movie_id = str(data.get("movie_id"))
    status = data.get("movie_status")

    existing_status = MovieStatus.query.filter_by(user_id=user_id, movie_id=movie_id).first()

    if not existing_status:
        status = MovieStatus(user_id=user_id, movie_id=movie_id, status= status)
        database.session.add(status)
    else:
        existing_status.status = status

    database.session.commit()

    return jsonify({"message": "Выбор сохранен", "movie_status": data.get("movie_status"), "movie_id": data.get("movie_id")})

@main.route("/search/<term>")
def search_movie_page(term):
    if not session.get('current_page'):
        session['current_page'] = 1
    search_results = search_movie(term,page=session['current_page'])
    return render_template("search_results_page.html", search_results=search_results,current_page=session['current_page'],term=term)


