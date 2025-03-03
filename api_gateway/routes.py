from flask import Blueprint, request, jsonify
import requests

gateway_bp = Blueprint("gateway", __name__)

AUTH_SERVICE_URL = "http://localhost:5001/auth"
COMMENTS_SERVICE_URL = "http://localhost:5003/comments"
MOVIE_STATUS_SERVICE_URL = "http://localhost:5002/movie_status"

@gateway_bp.route("/register", methods=["POST"])
def register():
    response = requests.post(f"{AUTH_SERVICE_URL}/register", json=request.json)
    return jsonify(response.json()), response.status_code

@gateway_bp.route("/login", methods=["POST"])
def login():
    response = requests.post(f"{AUTH_SERVICE_URL}/login", json=request.json)
    return jsonify(response.json()), response.status_code

@gateway_bp.route("/add_comment", methods=["POST"])
def add_comment():
    response = requests.post(f"{COMMENTS_SERVICE_URL}/add_comment", json=request.json)
    return jsonify(response.json()), response.status_code

@gateway_bp.route("/get_comments", methods=["GET"])
def get_comments():
    movie_id = request.args.get("movie_id")

    response = requests.get(f"{COMMENTS_SERVICE_URL}/get_comments",params={"movie_id":movie_id})
    return jsonify(response.json()), response.status_code

@gateway_bp.route("/like_comment", methods=["PATCH"])
def like_comment():
    response = requests.patch(f"{COMMENTS_SERVICE_URL}/like_comment", json=request.json)
    return jsonify(response.json()), response.status_code

@gateway_bp.route("/dislike_comment", methods=["PATCH"])
def dislike_comment():
    response = requests.patch(f"{COMMENTS_SERVICE_URL}/dislike_comment", json=request.json)
    return jsonify(response.json()), response.status_code

@gateway_bp.route("/get_movie_status", methods=["GET"])
def get_movie_status():
    movie_id = request.args.get("movie_id")
    user_id = request.args.get("user_id")

    response = requests.get(f"{MOVIE_STATUS_SERVICE_URL}/get_movie_status", params={"movie_id": movie_id, "user_id": user_id})
    return jsonify(response.json()), response.status_code

@gateway_bp.route("/save_movie_status",methods=["POST"])
def save_movie_status():
    response = requests.post(f"{MOVIE_STATUS_SERVICE_URL}/save_movie_status", json=request.json)
    return jsonify(response.json()), response.status_code

@gateway_bp.route("/get_movie_statuses_count", methods=["GET"])
def get_movie_statuses_count():
    user_id = request.args.get("user_id")

    response = requests.get(f"{MOVIE_STATUS_SERVICE_URL}/get_movie_statuses_count", params={"user_id": user_id})
    return jsonify(response.json()), response.status_code

@gateway_bp.route("/get_movie_statuses", methods=["GET"])
def get_movie_statuses():
    user_id = request.args.get("user_id")

    response = requests.get(f"{MOVIE_STATUS_SERVICE_URL}/get_movie_statuses", params={"user_id": user_id})
    return jsonify(response.json()), response.status_code