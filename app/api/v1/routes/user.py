from fastapi import APIRouter, Depends

from app.core.dependencies import get_current_user, require_role
from app.models.user import User
from app.schemas.common import MessageResponse
from app.schemas.user import UserResponse

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    """
    Endpoint protegido
    Solo usuario con token valido pueden acceder
    """
    return current_user


@router.get("/admin", response_model=MessageResponse)
def admin_only(user=Depends(require_role("admin"))):
    """
    Solo accesible para admins
    """
    return {"message": "Welcome admin"}
