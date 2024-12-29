from flask import (
    Blueprint,
    render_template,
    request
)

from mtg_deck_editor.domain.models import ValidationError

bp = Blueprint("errors", __name__)

@bp.errorhandler(Exception)
def unknown_error(error: Exception):
    if request.accept_mimetypes.accept_json:
        return { "error": 500, "message": "Unknown error."}, 500
    return render_template("errors/unknown.html"), 500

@bp.errorhandler(ValidationError)
def validation_error(error: ValidationError):
    if request.accept_mimetypes.accept_json:
        return { "error": 400, "message": "Unknown error."}, 400
    return render_template("errors/validation.html"), 400