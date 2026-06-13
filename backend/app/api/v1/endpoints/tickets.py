import uuid
from typing import Annotated

from fastapi import APIRouter, Query, Response, status, Depends

from app.api.deps import TicketServiceDep, get_current_user
from app.schemas.ticket import (
    TicketCategory,
    TicketCreate,
    TicketListResponse,
    TicketPriority,
    TicketRead,
    TicketSentiment,
    TicketStatus,
    TicketStatusUpdate,
)

router = APIRouter(dependencies=[Depends(get_current_user)])


@router.post("", response_model=TicketRead, status_code=status.HTTP_201_CREATED)
def create_ticket(ticket_in: TicketCreate, ticket_service: TicketServiceDep) -> TicketRead:
    return ticket_service.create_ticket(ticket_in)


@router.get("", response_model=TicketListResponse)
def list_tickets(
    ticket_service: TicketServiceDep,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
    offset: Annotated[int, Query(ge=0)] = 0,
    status_filter: Annotated[TicketStatus | None, Query(alias="status")] = None,
    priority: TicketPriority | None = None,
    category: TicketCategory | None = None,
    sentiment: TicketSentiment | None = None,
) -> TicketListResponse:
    return ticket_service.list_tickets(
        limit=limit,
        offset=offset,
        status=status_filter,
        priority=priority,
        category=category,
        sentiment=sentiment,
    )


@router.get("/{ticket_id}", response_model=TicketRead)
def get_ticket(ticket_id: uuid.UUID, ticket_service: TicketServiceDep) -> TicketRead:
    return ticket_service.get_ticket(ticket_id)


@router.patch("/{ticket_id}/status", response_model=TicketRead)
def update_ticket_status(
    ticket_id: uuid.UUID,
    status_update: TicketStatusUpdate,
    ticket_service: TicketServiceDep,
) -> TicketRead:
    return ticket_service.update_status(ticket_id, status_update.status)


@router.post("/{ticket_id}/predict", response_model=TicketRead)
def rerun_prediction(ticket_id: uuid.UUID, ticket_service: TicketServiceDep) -> TicketRead:
    return ticket_service.rerun_prediction(ticket_id)


@router.delete("/{ticket_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_ticket(ticket_id: uuid.UUID, ticket_service: TicketServiceDep) -> Response:
    ticket_service.delete_ticket(ticket_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
