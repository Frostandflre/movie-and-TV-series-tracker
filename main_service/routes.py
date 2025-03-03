from flask import render_template, redirect,url_for,Blueprint,session,flash,make_response,request,jsonify
from .forms import RegistrationForm,AuthorizationForm,CommentForm
from .movie_logic import get_movie_info, get_popular_movies, search_movie, get_similar_movies
import requests

main = Blueprint('main', __name__)

API_GATEWAY_URL = "http://localhost:5005"

@main.route("/")
def main_page():
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
def login_page():
    nickname = "Guest"
    if 'nickname' in request.cookies:
        nickname = request.cookies.get('nickname')
    form = AuthorizationForm()
    if form.validate_on_submit():
        user_data = {
            'email': form.email.data,
            'password': form.password.data
        }

        login_response = requests.post(f"{API_GATEWAY_URL}/login", json=user_data)

        if login_response.status_code == 400:
            flash("Неправильный email или пароль!", "error")
            return redirect(url_for('main.login_page'))

        if login_response.status_code != 200:
            flash("Ошибка входа. Попробуйте позже.", "error")
            return redirect(url_for('main.login_page'))

        user_info = login_response.json()

        nickname = user_info["nickname"]
        user_id = str(user_info["user_id"])

        save_cookie_response = make_response(redirect(url_for('main.main_page')))
        save_cookie_response.set_cookie('nickname', nickname,max_age=60*60*24*30, secure=True, httponly=True,)
        save_cookie_response.set_cookie('user_id', user_id, max_age=60*60*24*30, secure=True, httponly=True, )
        return save_cookie_response
    return render_template('login_page.html', form=form,nickname=nickname)

@main.route("/logout")
def logout_page():
    logout_response = make_response(redirect(url_for('main.main_page')))
    logout_response.set_cookie('nickname', '', expires=0)
    logout_response.set_cookie('user_id', '', expires=0)
    return logout_response

@main.route("/registration",methods=['GET', 'POST'])
def registration_page():
    nickname = "Guest"
    if 'nickname' in request.cookies:
        nickname = request.cookies.get('nickname')
    form = RegistrationForm()
    if form.validate_on_submit():
        user_data = {
            'nickname': form.nickname.data,
            'email': form.email.data,
            'password': form.password.data
        }

        registration_response = requests.post(f"{API_GATEWAY_URL}/register", json=user_data)

        if registration_response.status_code == 400:
            flash("Email уже зарегистрирован", "error")
            return render_template("registration_page.html", form=form)

        if registration_response.status_code != 200:
            flash("Ошибка регистрации. Попробуйте позже.", "error")
            return render_template("registration_page.html", form=form)

        user_info = registration_response.json()

        nickname = user_info["nickname"]
        user_id = str(user_info["user_id"])

        save_cookie_response = make_response(redirect(url_for('main.main_page')))
        save_cookie_response.set_cookie('nickname', nickname, max_age=60 * 60 * 24 * 30, secure=True, httponly=True, )
        save_cookie_response.set_cookie('user_id', user_id, max_age=60 * 60 * 24 * 30, secure=True, httponly=True, )
        return save_cookie_response
    return render_template("registration_page.html",form=form,nickname=nickname)

@main.route("/movie_info/<movie_id>",methods=['GET','POST'])
def movie_info_page(movie_id):
    nickname = "Guest"
    if 'nickname' in request.cookies:
        nickname = request.cookies.get('nickname')
    user_id = request.cookies.get('user_id')

    get_status_response = requests.get(f"{API_GATEWAY_URL}/get_movie_status",params={"movie_id":movie_id,"user_id":user_id})

    if get_status_response.status_code == 404:
        flash("Фильм не найден", "error")
        return redirect(url_for('main.main_page'))

    if get_status_response.status_code == 200:
        current_status = get_status_response.json()["status"]
    elif get_status_response.status_code == 401:
        current_status = "Не просмотрено"
    else:
        flash("Ошибка получения статуса просмотра", "error")
        return redirect(url_for('main.main_page'))
    movie_info = get_movie_info(movie_id)
    similar_movies = get_similar_movies(movie_id)

    get_comments_response = requests.get(f"{API_GATEWAY_URL}/get_comments",params={"movie_id":movie_id})


    movie_comments = get_comments_response.json()['comments']

    form = CommentForm()
    if form.validate_on_submit():
        comment_data = {
            "comment": form.comment.data,
            "movie_id": movie_id,
            "nickname": nickname,
            "user_id": user_id,
            "movie_title": movie_info["title"]
        }
        add_comment_response = requests.post(f"{API_GATEWAY_URL}/add_comment", json=comment_data)
        if add_comment_response.status_code == 401:
            flash("Пользователь не авторизован", "error")
            return redirect(url_for("main.movie_info_page",movie_id=movie_id))

        if add_comment_response.status_code == 400:
            flash("Поле добавления комментария пустое", "error")
            return redirect(url_for("main.movie_info_page",movie_id=movie_id))

        if add_comment_response.status_code!= 200:
            flash("Ошибка добавления комментария. Попробуйте позже.", "error")
            return redirect(url_for("main.movie_info_page", movie_id=movie_id))

        return redirect(url_for("main.movie_info_page",movie_id=movie_id))

    return render_template("movie_info_page.html",nickname=nickname,movie_info=movie_info,movie_id=movie_id,current_status=current_status,form=form,movie_comments=movie_comments,similar_movies=similar_movies)

@main.route("/save_movie_status", methods=["POST"])
def save_movie_status():
    data = request.get_json()

    status_data = {
        "status" : data.get("movie_status"),
        "user_id" : request.cookies.get('user_id'),
        "movie_id" : str(data.get("movie_id")),
        "movie_title" : data.get("movie_title")
    }

    save_status_response = requests.post(f"{API_GATEWAY_URL}/save_movie_status", json=status_data)

    if save_status_response.status_code == 401:
        flash("Пользователь не авторизован", "error")
        return redirect(url_for("main.movie_info_page",movie_id=status_data["movie_id"]))

    if save_status_response.status_code == 400:
        flash("Некорректные данные", "error")
        return redirect(url_for("main.movie_info_page",movie_id=status_data["movie_id"]))

    if save_status_response.status_code!= 200:
        flash("Ошибка сохранения статуса просмотра. Попробуйте позже.", "error")
        return redirect(url_for("main.movie_info_page",movie_id=status_data["movie_id"]))


    return jsonify({"message": "Новый статус установлен"}),200

@main.route("/like_comment",methods=["PATCH"])
def like_comment():
    data = request.get_json()

    comment_data = {
    "comment_id": data.get("comment_id"),
    "movie_id": data.get("movie_id"),
    "user_id": request.cookies.get('user_id')
    }

    like_comment_response = requests.patch(f"{API_GATEWAY_URL}/like_comment", json=comment_data)

    if like_comment_response.status_code == 401:
        flash("Пользователь не авторизован", "error")
        return jsonify({"message": "Пользователь не авторизован"}),401

    if like_comment_response.status_code == 400:
        flash("Некорректные данные", "error")
        return jsonify({"message": "Некорректные данные"}), 400

    if like_comment_response.status_code!= 200:
        flash("Ошибка постановки лайка. Попробуйте позже.", "error")
        return jsonify({"Ошибка постановки лайка. Попробуйте позже."}), 500

    return jsonify({"message": "Лайк поставлен"}),200

@main.route("/dislike_comment",methods=["PATCH"])
def dislike_comment():
    data = request.get_json()

    comment_data = {
    "comment_id": data.get("comment_id"),
    "movie_id": data.get("movie_id"),
    "user_id": request.cookies.get('user_id')
    }

    dislike_comment_response = requests.patch(f"{API_GATEWAY_URL}/dislike_comment", json=comment_data)

    if dislike_comment_response.status_code == 401:
        flash("Пользователь не авторизован", "error")
        return jsonify({"message": "Пользователь не авторизован"}),401

    if dislike_comment_response.status_code == 400:
        flash("Некорректные данные", "error")
        return jsonify({"message": "Некорректные данные"}),400

    if dislike_comment_response.status_code!= 200:
        flash("Ошибка постановки дизлайка. Попробуйте позже.", "error")
        return jsonify({"message": "Ошибка постановки дизлайка. Попробуйте позже."}),500

    return jsonify({"message": "Дизлайк поставлен"}),200

@main.route("/search/<term>")
def search_movie_page(term):
    if not session.get('current_page'):
        session['current_page'] = 1
    search_results = search_movie(term,page=session['current_page'])
    return render_template("search_results_page.html", search_results=search_results,current_page=session['current_page'],term=term)

@main.route("/profile")
def profile_page():
    user_id = request.cookies.get('user_id')

    movie_statuses_response = requests.get(f"{API_GATEWAY_URL}/get_movie_statuses_count",params={"user_id":user_id})

    if movie_statuses_response.status_code == 401:
        flash("Пользователь не авторизован", "error")
        return redirect(url_for('main.main_page'))

    if movie_statuses_response.status_code!= 200:
        flash("Ошибка получения статусов просмотра", "error")
        return redirect(url_for('main.main_page'))

    movie_statuses = movie_statuses_response.json()["movie_statuses"]

    return render_template("profile_page.html",nickname=request.cookies.get('nickname'),movie_statuses=movie_statuses)

@main.route("/profile/movie_list")
def movie_list_page():
    user_id = request.cookies.get('user_id')

    movie_statuses_response = requests.get(f"{API_GATEWAY_URL}/get_movie_statuses", params={"user_id": user_id})

    if movie_statuses_response.status_code == 401:
        flash("Пользователь не авторизован", "error")
        return redirect(url_for('main.main_page'))

    if movie_statuses_response.status_code!= 200:
        flash("Ошибка получения статусов просмотра", "error")
        return redirect(url_for('main.profile_page'))
    print(movie_statuses_response.text)
    movie_statuses = movie_statuses_response.json()["movie_statuses"]

    return render_template("movie_list_page.html", watched_movie_list=movie_statuses["watched_movie_list"],planned_movie_list=movie_statuses["planned_movie_list"],dropped_movie_list=movie_statuses["dropped_movie_list"],in_process_movie_list=movie_statuses["in_process_movie_list"])





