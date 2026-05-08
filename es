[1mdiff --git a/app/api/v1/routes/auth.py b/app/api/v1/routes/auth.py[m
[1mindex 233a0..dbf47 100644[m
[1m--- a/app/api/v1/routes/auth.py[m
[1m+++ b/app/api/v1/routes/auth.py[m
[36m@@ -1,12 +1,15 @@[m
 from fastapi import APIRouter, Depends, HTTPException[m
[32m+[m[32mfrom fastapi.security import HTTPAuthorizationCredentials, HTTPBearer[m
 from sqlalchemy.orm import Session[m
 [m
 from app.core.security import create_token, decode_token[m
 from app.db.session import SessionLocal[m
[32m+[m[32mfrom app.models.token_blacklist import TokenBlacklist[m
 from app.schemas.user import TokenRefresh, UserCreate, UserLogin[m
 from app.services.auth_service import login, register[m
 [m
 router = APIRouter(prefix="/auth", tags=["Auth"])[m
[32m+[m[32msecurity = HTTPBearer()[m
 [m
 [m
 def get_db():[m
[36m@@ -50,3 +53,20 @@[m [mdef refresch_token(data: TokenRefresh):[m
         })[m
     [m
     return {"access_token": new_access_token}[m
[32m+[m
[32m+[m
[32m+[m[32m@router.post("/logout")[m
[32m+[m[32mdef logout([m
[32m+[m[32m    credentials: HTTPAuthorizationCredentials = Depends(security),[m
[32m+[m[32m    db: Session = Depends(get_db),[m
[32m+[m[32m):[m
[32m+[m[32m    token = credentials.credentials[m
[32m+[m
[32m+[m[32m    # Si ya está en blacklist, lo tratamos como logout idempotente[m
[32m+[m[32m    exists = db.query(TokenBlacklist).filter(TokenBlacklist.token == token).first()[m
[32m+[m[32m    if exists:[m
[32m+[m[32m        return {"message": "Logged out"}[m
[32m+[m
[32m+[m[32m    db.add(TokenBlacklist(token=token))[m
[32m+[m[32m    db.commit()[m
[32m+[m[32m    return {"message": "Logged out"}[m
