from flask import (
    Blueprint,
    render_template,
    request
)

from mtg_deck_editor.domain.models import ValidationError

bp = Blueprint("errors", __name__)


@bp.app_errorhandler(ValidationError)
def validation_error(error: ValidationError):
    if request.accept_mimetypes.accept_json and not request.accept_mimetypes.accept_html:
        return { "error": 400, "message": error.message}, 400
    return "", 400 #TODO

@bp.app_errorhandler(404)
def not_found_error(error):
    if request.accept_mimetypes.accept_json and not request.accept_mimetypes.accept_html:
        return { "error": 404, "message": "Resource not found."}, 404
    return render_template("errors/404.html"), 404

@bp.app_errorhandler(500)
def unknown_error(error):
    if request.accept_mimetypes.accept_json and not request.accept_mimetypes.accept_html:
        return { "error": 500, "message": "Unknown error."}, 500
    return render_template("errors/500.html"), 500
