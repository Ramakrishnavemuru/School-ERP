from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from backend.app.database import get_db
from backend.app.models.user import User
from backend.app.schemas.auth import LoginRequest, Token, PasswordChangeRequest
from backend.app.schemas.user import UserResponse
from backend.app.services.auth_service import auth_service
from backend.app.utils.security import create_access_token
from backend.app.utils.permissions import get_current_active_user
from backend.app.utils.helpers import log_audit_action

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/login", response_model=Token)
def login(login_data: LoginRequest, request: Request, db: Session = Depends(get_db)):
    user = auth_service.authenticate_user(db, login_data.username, login_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is disabled"
        )

    access_token = create_access_token(
        data={"sub": str(user.id), "role": user.role}
    )

    # Attach profile id if available
    profile_id = None
    if user.role == "STUDENT" and user.student_profile:
        profile_id = user.student_profile.id
    elif user.role == "TEACHER" and user.teacher_profile:
        profile_id = user.teacher_profile.id
    elif user.role == "PARENT" and user.parent_profile:
        profile_id = user.parent_profile.id
    elif user.role == "PRINCIPAL" and user.principal_profile:
        profile_id = user.principal_profile.id

    client_ip = request.client.host if request.client else None
    log_audit_action(db, "LOGIN", "User", str(user.id), f"User {user.username} logged in", user.id, client_ip)

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "full_name": user.full_name,
            "role": user.role,
            "profile_id": profile_id,
            "avatar": user.avatar
        }
    }

@router.get("/me")
def get_current_user_profile(
    current_user: User = Depends(get_current_active_user)
):
    profile_id = None
    extra = {}
    if current_user.role == "STUDENT" and current_user.student_profile:
        profile_id = current_user.student_profile.id
        extra = {
            "admission_number": current_user.student_profile.admission_number,
            "roll_number": current_user.student_profile.roll_number,
            "class_id": current_user.student_profile.class_id,
            "section_id": current_user.student_profile.section_id,
            "class_name": current_user.student_profile.class_obj.name if current_user.student_profile.class_obj else None,
            "section_name": current_user.student_profile.section.name if current_user.student_profile.section else None,
        }
    elif current_user.role == "TEACHER" and current_user.teacher_profile:
        profile_id = current_user.teacher_profile.id
        extra = {
            "employee_id": current_user.teacher_profile.employee_id,
            "designation": current_user.teacher_profile.designation,
            "department_id": current_user.teacher_profile.department_id,
            "department_name": current_user.teacher_profile.department.name if current_user.teacher_profile.department else None,
        }
    elif current_user.role == "PARENT" and current_user.parent_profile:
        profile_id = current_user.parent_profile.id
        extra = {
            "children_count": len(current_user.parent_profile.students)
        }
    elif current_user.role == "PRINCIPAL" and current_user.principal_profile:
        profile_id = current_user.principal_profile.id
        extra = {
            "employee_id": current_user.principal_profile.employee_id
        }

    return {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email,
        "full_name": current_user.full_name,
        "role": current_user.role,
        "is_active": current_user.is_active,
        "phone": current_user.phone,
        "avatar": current_user.avatar,
        "profile_id": profile_id,
        "created_at": current_user.created_at,
        **extra
    }

@router.post("/change-password")
def change_password(
    data: PasswordChangeRequest,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    auth_service.change_password(db, current_user, data.old_password, data.new_password)
    log_audit_action(db, "PASSWORD_CHANGE", "User", str(current_user.id), "Password updated", current_user.id)
    return {"message": "Password changed successfully"}

@router.post("/logout")
def logout(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    log_audit_action(db, "LOGOUT", "User", str(current_user.id), "User logged out", current_user.id)
    return {"message": "Successfully logged out"}
