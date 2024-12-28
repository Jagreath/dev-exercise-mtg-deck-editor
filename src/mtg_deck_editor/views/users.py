from flask import (
    Blueprint
)

bp = Blueprint("users", __name__)

@bp.route("/users/<username>")
def user(username):
    pass