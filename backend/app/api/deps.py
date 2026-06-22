from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.services.ticket_service import TicketService
from app.models.user import User
from app.core.security import decode_access_token

DbSession = Annotated[Session, Depends(get_db)]

def get_ticket_service(db: DbSession) -> TicketService:
    return TicketService(db)

TicketServiceDep = Annotated[TicketService, Depends(get_ticket_service)]

# oauth2_scheme points to the login endpoint
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)], 
    db: DbSession
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    payload = decode_access_token(token)
    if payload is None:
        raise credentials_exception
        
    username: str = payload.get("sub")
    if username is None:
        raise credentials_exception
        
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise credentials_exception
        
    return user

CurrentUser = Annotated[User, Depends(get_current_user)]

def get_current_admin(current_user: CurrentUser) -> User:
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The user does not have enough privileges",
        )
    return current_user

CurrentAdmin = Annotated[User, Depends(get_current_admin)]
