from fastapi import APIRouter, Depends

from app.core.dependencies import get_current_user, require_role

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me")
def get_me(current_user=Depends(get_current_user)):
    """
    Enpoint protegido
    Solo usuario con token valido pueden acceder
    """
    return {"id": current_user.id, "email": current_user.email}


@router.get("/admin")
def admin_only(user=Depends(require_role("admin"))):
    """
    Solo accesible para admins
    """
    return {"message": "Welcome admin"}
