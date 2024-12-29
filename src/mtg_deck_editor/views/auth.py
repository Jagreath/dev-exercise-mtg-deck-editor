from datetime import datetime, timezone
import functools
from flask import (
    Blueprint,
    redirect,
    render_template,
    request,
    session,
    url_for,
    g
)

from mtg_deck_editor.domain.models import User, ValidationError
from mtg_deck_editor.infrastructure.repos import UserRepository


bp = Blueprint("auth", __name__)

@bp.before_app_request
def load_user_from_session():
    user_id = session.get("user_id")
    if user_id is None:
        g.user = None
    else:
        repo = UserRepository()
        g.user = repo.get_by_uuid(user_id)
        if g.user:
            g.user.accessed = datetime.now(timezone.utc)
            repo.save()

def authorized(view):
    @functools.wraps(view)
    def wrapped(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login', next=request.path))
        return view(**kwargs)

    return wrapped

def anonymous(view):
    @functools.wraps(view)
    def wrapped(**kwargs):
        if g.user is not None:
            return redirect(url_for('home.index'))
        return view(**kwargs)

    return wrapped

@bp.get("/login")
@anonymous
def login():
    return render_template("auth/login.html")

@bp.post("/login")
@anonymous
def login_post():
    repo = UserRepository()

    username = request.form["username"]

    user = repo.get_by_name(username)
    if user is None:
        raise ValidationError("Incorrect username.")

    if user.validate_password(password=request.form["password"]):
        session.clear()
        session["user_id"] = user.uuid
        return redirect(request.args.get("next", url_for("home.index")))
    else:
        raise ValidationError("Incorrect password.")

@bp.get("/logout")
@authorized
def logout():
    session.clear()
    return redirect(request.args.get("next", url_for("home.index")))

@bp.get("/register")
@anonymous
def register():
    return render_template("auth/register.html")

@bp.post("/register")
@anonymous
def register_post():
    repo = UserRepository()
    username = request.form["username"]

    user = repo.get_by_name(username)
    if user is not None:
        raise ValidationError("Username already exists.")
    
    user = User.new(username, request.form["password"])
    repo.add(user)
    repo.save()
    return redirect(url_for("auth.login"))