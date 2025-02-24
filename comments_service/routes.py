from flask import Blueprint, request, jsonify
from .models import Comments
from db_extensions import database


comments_bp = Blueprint("comments", __name__)

@comments_bp.route("/add_comment", methods=["POST"])
def add_comment():
    comment_data = request.json

    if not comment_data['user_id'] or  comment_data['nickname'] == "Guest":
        return jsonify({"error": "Пользователь не авторизован"}), 401

    if not comment_data['comment']:
        return jsonify({"error": "Некорректные данные"}), 400

    comment = Comments(text=comment_data['comment'], author_nickname=comment_data['nickname'], user_id=comment_data['user_id'], movie_id=comment_data['movie_id'])

    database.session.add(comment)
    database.session.commit()
    return jsonify({"message": "Комментарий добавлен"}), 200


@comments_bp.route('/get_comments', methods=['GET'])
def get_comments():
    movie_id = request.args.get("movie_id")
    if not movie_id:
        return jsonify({"error": "Некорректные данные"}), 400
    comments = Comments.query.filter_by(movie_id=movie_id).all()
    return jsonify({"message": "Комментарии получены","comments":[comment.to_dict() for comment in comments]}),200
