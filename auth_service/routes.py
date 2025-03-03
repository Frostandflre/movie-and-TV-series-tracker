from flask import Blueprint, request, jsonify
from .models import Users
from db_extensions import database
from werkzeug.security import generate_password_hash, check_password_hash

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.json
    if Users.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email уже зарегистрирован'}), 400

    hashed_password = generate_password_hash(data["password"],salt_length=128)
    new_user = Users(nickname=data["nickname"],password=hashed_password, email=data["email"])
    database.session.add(new_user)
    database.session.commit()
    return jsonify({"message": "Пользователь зарегистрирован","user_id":new_user.user_id,"nickname": new_user.nickname}), 200


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    user = Users.query.filter_by(email=data["email"]).first()

    if not user or not check_password_hash(user.password, data['password']):
        return jsonify({"error": "Неправильный логин или пароль"}), 400
    return jsonify({"message": "Вход выполнен","user_id": user.user_id, "nickname": user.nickname}),200
