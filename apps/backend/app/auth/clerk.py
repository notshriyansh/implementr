from fastapi import HTTPException
from fastapi import Request
from fastapi import status

from clerk_backend_api import (
    AuthenticateRequestOptions,
    authenticate_request,
)

from app.auth.current_user import CurrentUser

from app.core.config import get_settings

settings = get_settings()


AUTHORIZED_PARTIES = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]





def get_current_user(
    request: Request,
) -> CurrentUser:
    request_state = authenticate_request(
        request,
        AuthenticateRequestOptions(
            secret_key=settings.clerk_secret_key,
            jwt_key=settings.clerk_jwt_key,
            authorized_parties=AUTHORIZED_PARTIES,
            accepts_token=["session_token"],
        ),
    )

    if not request_state.is_signed_in:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=(
                request_state.reason.name
                if request_state.reason
                else "AUTHENTICATION_REQUIRED"
            ),
            headers={"WWW-Authenticate": "Bearer"},
        )

    payload = request_state.payload
    user_id = payload.get("sub") if payload else None

    if not isinstance(user_id, str):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="AUTHENTICATION_REQUIRED",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return CurrentUser(user_id=user_id)
