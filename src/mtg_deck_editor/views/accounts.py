from flask import (
    Blueprint,
    redirect,
    render_template,
    request,
    session,
    url_for,
    g
)

from mtg_deck_editor.infra.repos import make_user_repo
from mtg_deck_editor.domain.models import (User)


bp = Blueprint("accounts", __name__)

@bp.before_app_request
def load_user_from_session():
    user_id = session.get("user_id")
    if user_id is None:
        g.user = None
    else:
        repo = make_user_repo()
        g.user = repo.get_by_uuid(user_id)

@bp.get("/login")
def login():
    return render_template("accounts/login.html")

@bp.post("/login")
def login_post():
    repo = make_user_repo()

    username = request.form["username"]
    # next = request.args.get('next','/')

    user = repo.get_by_name(username)
    if user is None:
        raise "Incorrect username."

    if user.validate_password(password=request.form["password"]):
        session.clear()
        session["user_id"] = user.uuid
        return redirect(request.args.get("next", url_for("home.index")))
    else:
        raise "Incorrect password."

@bp.get("/logout")
def logout():
    session.clear()
    return redirect(request.args.get("next", url_for("home.index")))

@bp.get("/register")
def register():
    return render_template("accounts/register.html")

@bp.post("/register")
def register_post():
    repo = make_user_repo()
    username = request.form["username"]

    user = repo.get_by_name(username)
    if user is not None:
        raise ValueError("Username already exists.")
    
    user = User(name = username, password = request.form["password"])
    repo.add(user)
    repo.save()
    return redirect(url_for("accounts.login"))