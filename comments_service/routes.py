from flask import Blueprint, request, jsonify
from .models import Comments,CommentReaction
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
    comments = Comments.query.filter_by(movie_id=movie_id).order_by(Comments.likes.desc()).all()
    return jsonify({"message": "Комментарии получены","comments":[comment.to_dict() for comment in comments]}),200

@comments_bp.route('/like_comment', methods=['PATCH'])
def like_comment():
    data = request.json

    if not data["user_id"]:
        return jsonify({"error": "Пользователь не авторизован"}), 401

    if not data["comment_id"] or not data["movie_id"]:
        return jsonify({"error": "Некорректные данные"}), 400

    comment = Comments.query.filter_by(id=data["comment_id"], movie_id=data["movie_id"]).first()

    if not comment:
        return jsonify({"error": "Комментарий не найден"}), 404

    existing_reaction = CommentReaction.query.filter_by(comment_id=data["comment_id"],user_id=data["user_id"]).first()

    if existing_reaction:
        if existing_reaction.reaction_type == "like":
            return jsonify({"message": "Лайк поставлен"}), 200
        else:
            existing_reaction.reaction_type = "like"
            comment.likes += 1
            comment.dislikes -= 1

    else:
        reaction = CommentReaction(comment_id=data["comment_id"], user_id=data["user_id"], reaction_type="like")
        comment.likes += 1
        database.session.add(reaction)

    database.session.commit()
    return jsonify({"message": "Лайк поставлен"}), 200

@comments_bp.route('/dislike_comment', methods=['PATCH'])
def dislike_comment():
    data = request.json

    if not data["user_id"]:
        return jsonify({"error": "Пользователь не авторизован"}), 401

    if not data["comment_id"] or not data["movie_id"]:
        return jsonify({"error": "Некорректные данные"}), 400

    comment = Comments.query.filter_by(id=data["comment_id"], movie_id=data["movie_id"]).first()

    if not comment:
        return jsonify({"error": "Комментарий не найден"}), 404

    existing_reaction = CommentReaction.query.filter_by(comment_id=data["comment_id"],user_id=data["user_id"]).first()

    if existing_reaction:
        if existing_reaction.reaction_type == "dislike":
            return jsonify({"message": "Дизлайк поставлен"}), 200
        else:
            existing_reaction.reaction_type = "dislike"
            comment.likes -= 1
            comment.dislikes += 1

    else:
        reaction = CommentReaction(comment_id=data["comment_id"], user_id=data["user_id"], reaction_type="dislike")
        comment.dislikes += 1
        database.session.add(reaction)

    database.session.commit()
    return jsonify({"message": "Дизлайк поставлен"}), 200