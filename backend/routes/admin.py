from flask import Blueprint

from backend.models.model_enums import UserRole
from backend.utils.decorators import role_required
from backend.utils.responses import success_response

admin_bp = Blueprint(name="admin", import_name=__name__, url_prefix="/api/admin")


@admin_bp.get("/test")
@role_required(UserRole.ADMIN)
def test():

    return success_response(message="Admin access granted")
