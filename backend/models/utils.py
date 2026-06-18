from backend.models.user import User
from backend.extensions import db


def delete_from_db(user_id: int) -> bool:
    """
    Deletes user from user table and corresponding entry from student or company table and returns deletion status
    """
    user = User.query.get(user_id)
    if user:
        try:
            db.session.delete(user)
            db.session.flush()
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
    return False
