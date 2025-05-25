from flask import Blueprint, jsonify

from app.app_hello.models import MESSAGES


hello = Blueprint("hello", __name__)


@hello.route("/")
@hello.route("/hello", methods=["GET"])
def hello():
    return MESSAGES, 200
