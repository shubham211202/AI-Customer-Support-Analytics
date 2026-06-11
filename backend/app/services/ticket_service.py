import uuid

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.ticket import Ticket
from app.repositories.ticket_repository import TicketRepository
from app.schemas.prediction import PredictionRead
from app.schemas.ticket import TicketCreate, TicketListResponse, TicketRead
from app.services.prediction_service import PredictionService


class TicketService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.repository = TicketRepository(db)
        self.prediction_service = PredictionService()

    def create_ticket(self, ticket_in: TicketCreate) -> TicketRead:
        ticket = self.repository.create_ticket(ticket_in)
        prediction_in = self.prediction_service.predict(
            subject=ticket.subject,
            description=ticket.description,
        )
        self.repository.create_prediction(ticket.id, prediction_in)
        self.db.commit()
        self.db.refresh(ticket)
        return self._to_read_model(ticket)

    def list_tickets(
        self,
        *,
        limit: int,
        offset: int,
        status: str | None = None,
        priority: str | None = None,
        category: str | None = None,
        sentiment: str | None = None,
    ) -> TicketListResponse:
        tickets, total = self.repository.list_tickets(
            limit=limit,
            offset=offset,
            status=status,
            priority=priority,
            category=category,
            sentiment=sentiment,
        )
        return TicketListResponse(
            items=[self._to_read_model(ticket) for ticket in tickets],
            limit=limit,
            offset=offset,
            total=total,
        )

    def get_ticket(self, ticket_id: uuid.UUID) -> TicketRead:
        ticket = self._get_existing_ticket(ticket_id)
        return self._to_read_model(ticket)

    def update_status(self, ticket_id: uuid.UUID, new_status: str) -> TicketRead:
        ticket = self._get_existing_ticket(ticket_id)
        self.repository.update_status(ticket, new_status)
        self.db.commit()
        self.db.refresh(ticket)
        return self._to_read_model(ticket)

    def rerun_prediction(self, ticket_id: uuid.UUID) -> TicketRead:
        ticket = self._get_existing_ticket(ticket_id)
        prediction_in = self.prediction_service.predict(
            subject=ticket.subject,
            description=ticket.description,
        )
        self.repository.create_prediction(ticket.id, prediction_in)
        self.db.commit()
        self.db.refresh(ticket)
        return self._to_read_model(ticket)

    def delete_ticket(self, ticket_id: uuid.UUID) -> None:
        ticket = self._get_existing_ticket(ticket_id)
        self.repository.soft_delete(ticket)
        self.db.commit()

    def _get_existing_ticket(self, ticket_id: uuid.UUID) -> Ticket:
        ticket = self.repository.get_ticket(ticket_id)
        if ticket is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Ticket not found",
            )
        return ticket

    @staticmethod
    def _to_read_model(ticket: Ticket) -> TicketRead:
        latest_prediction = ticket.predictions[0] if ticket.predictions else None
        return TicketRead(
            id=ticket.id,
            customer_id=ticket.customer_id,
            subject=ticket.subject,
            description=ticket.description,
            source=ticket.source,
            status=ticket.status,
            prediction=PredictionRead.model_validate(latest_prediction)
            if latest_prediction
            else None,
            created_at=ticket.created_at,
            updated_at=ticket.updated_at,
        )
