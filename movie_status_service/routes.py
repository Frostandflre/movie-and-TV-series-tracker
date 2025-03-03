from flask import Blueprint, request, jsonify
from .models import MovieStatus
from db_extensions import database


movie_status_bp = Blueprint("comments", __name__)

@movie_status_bp.route("/get_movie_status", methods=["GET"])
def get_movie_status():
    movie_id = request.args.get("movie_id")
    user_id = request.args.get("user_id")
    if not movie_id:
        return jsonify({"error": "Фильм не найден"}), 404

    if not user_id:
        return jsonify({"error": "Пользователь не авторизован"}), 401

    status_obj = MovieStatus.query.filter_by(user_id=user_id,movie_id=movie_id).first()

    if status_obj is None:
        status = "Не просмотрено"
    else:
        status = status_obj.status

    return jsonify({"message": "Статус получен","status":status}),200


@movie_status_bp.route("/save_movie_status", methods=["POST"])
def save_movie_status():
    status_data = request.json
    if not status_data['user_id']:
        return jsonify({"error": "Пользователь не авторизован"}), 401

    if not status_data['movie_id'] or not status_data["movie_title"] or not status_data["status"]:
        return jsonify({"error": "Некорректные данные"}), 400

    existing_status = MovieStatus.query.filter_by(user_id=status_data['user_id'], movie_id=status_data['movie_id']).first()

    if status_data["status"] == "Не просмотрено":
        if existing_status:
            database.session.delete(existing_status)
    else:
        if existing_status:
            existing_status.status = status_data["status"]
        else:
            status = MovieStatus(user_id=status_data['user_id'], movie_id=status_data['movie_id'], status=status_data["status"], movie_title=status_data["movie_title"])
            database.session.add(status)


    database.session.commit()

    return jsonify({"message": "Новый статус установлен"}),200

@movie_status_bp.route("/get_movie_statuses_count", methods=["GET"])
def get_movie_statuses_count():
    user_id = request.args.get("user_id")

    if not user_id:
        return jsonify({"error": "Пользователь не авторизован"}), 401

    movie_statuses = [
        ("Всего",MovieStatus.query.filter_by(user_id=user_id).count()),
        ("Просмотрено",MovieStatus.query.filter_by(user_id=user_id,status = "Просмотрено").count()),
        ("В процессе", MovieStatus.query.filter_by(user_id=user_id, status="В процессе").count()),
        ("В планах", MovieStatus.query.filter_by(user_id=user_id, status="В планах").count()),
        ("Брошено", MovieStatus.query.filter_by(user_id=user_id, status="Заброшено").count())
    ]

    return jsonify({"message": "Статусы получены","movie_statuses":movie_statuses}),200


@movie_status_bp.route("/get_movie_statuses", methods=["GET"])
def get_movie_statuses():
    user_id = request.args.get("user_id")

    if not user_id:
        return jsonify({"error": "Пользователь не авторизован"}), 401

    movie_statuses = {
        "in_process_movie_list" : [movie.to_dict() for movie in MovieStatus.query.filter_by(user_id=user_id,status="В процессе")],
        "planned_movie_list" : [movie.to_dict() for movie in MovieStatus.query.filter_by(user_id=user_id, status="В планах")],
        "watched_movie_list" : [movie.to_dict() for movie in MovieStatus.query.filter_by(user_id=user_id, status="Просмотрено")],
        "dropped_movie_list" : [movie.to_dict() for movie in MovieStatus.query.filter_by(user_id=user_id, status="Заброшено")]
    }

    return jsonify({"message": "Статусы получены","movie_statuses":movie_statuses}),200