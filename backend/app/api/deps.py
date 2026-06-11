from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services.ticket_service import TicketService

DbSession = Annotated[Session, Depends(get_db)]


def get_ticket_service(db: DbSession) -> TicketService:
    return TicketService(db)


TicketServiceDep = Annotated[TicketService, Depends(get_ticket_service)]
