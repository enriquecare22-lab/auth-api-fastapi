from fastapi import APIRouter, Depends

from app.core.dependencies import get_current_user

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me")
def get_me(current_user=Depends(get_current_user)):
    """
    Enpoint protegido
    Solo usuario con token valido pueden acceder
    """
    return {"id": current_user.id, "email": current_user.email}
