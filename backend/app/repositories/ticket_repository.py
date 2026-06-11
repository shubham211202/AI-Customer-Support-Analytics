import uuid
from datetime import UTC, datetime

from sqlalchemy import Select, func, select
from sqlalchemy.orm import Session, selectinload

from app.models.prediction import TicketPrediction
from app.models.ticket import Ticket
from app.schemas.prediction import PredictionCreate
from app.schemas.ticket import TicketCreate


class TicketRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create_ticket(self, ticket_in: TicketCreate) -> Ticket:
        ticket = Ticket(
            customer_id=ticket_in.customer_id,
            subject=ticket_in.subject,
            description=ticket_in.description,
            source=ticket_in.source,
            status="open",
        )
        self.db.add(ticket)
        self.db.flush()
        return ticket

    def create_prediction(
        self,
        ticket_id: uuid.UUID,
        prediction_in: PredictionCreate,
    ) -> TicketPrediction:
        prediction = TicketPrediction(ticket_id=ticket_id, **prediction_in.model_dump())
        self.db.add(prediction)
        self.db.flush()
        return prediction

    def get_ticket(self, ticket_id: uuid.UUID) -> Ticket | None:
        statement = (
            select(Ticket)
            .options(selectinload(Ticket.predictions))
            .where(Ticket.id == ticket_id, Ticket.deleted_at.is_(None))
        )
        return self.db.scalar(statement)

    def list_tickets(
        self,
        *,
        limit: int,
        offset: int,
        status: str | None = None,
        priority: str | None = None,
        category: str | None = None,
        sentiment: str | None = None,
    ) -> tuple[list[Ticket], int]:
        statement = select(Ticket).options(selectinload(Ticket.predictions)).where(
            Ticket.deleted_at.is_(None)
        )
        count_statement: Select[tuple[int]] = select(func.count(Ticket.id)).where(
            Ticket.deleted_at.is_(None)
        )

        if status:
            statement = statement.where(Ticket.status == status)
            count_statement = count_statement.where(Ticket.status == status)

        if priority or category or sentiment:
            statement = statement.join(TicketPrediction)
            count_statement = count_statement.join(TicketPrediction)
            if priority:
                statement = statement.where(TicketPrediction.priority == priority)
                count_statement = count_statement.where(TicketPrediction.priority == priority)
            if category:
                statement = statement.where(TicketPrediction.category == category)
                count_statement = count_statement.where(TicketPrediction.category == category)
            if sentiment:
                statement = statement.where(TicketPrediction.sentiment == sentiment)
                count_statement = count_statement.where(TicketPrediction.sentiment == sentiment)

        statement = statement.order_by(Ticket.created_at.desc()).limit(limit).offset(offset)
        tickets = list(self.db.scalars(statement).unique().all())
        total = self.db.scalar(count_statement) or 0
        return tickets, total

    def update_status(self, ticket: Ticket, status: str) -> Ticket:
        ticket.status = status
        ticket.updated_at = datetime.now(UTC)
        self.db.add(ticket)
        self.db.flush()
        return ticket

    def soft_delete(self, ticket: Ticket) -> None:
        ticket.deleted_at = datetime.now(UTC)
        ticket.updated_at = datetime.now(UTC)
        self.db.add(ticket)
        self.db.flush()
