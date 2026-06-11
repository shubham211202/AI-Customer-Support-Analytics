from fastapi.testclient import TestClient


def create_ticket(client: TestClient) -> dict:
    response = client.post(
        "/api/v1/tickets",
        json={
            "customer_id": "cust_123",
            "subject": "Unable to login",
            "description": "I cannot access my account after resetting my password.",
            "source": "web",
        },
    )
    assert response.status_code == 201
    return response.json()


def test_create_ticket_returns_prediction(client: TestClient) -> None:
    ticket = create_ticket(client)

    assert ticket["status"] == "open"
    assert ticket["prediction"]["category"] == "account_access"
    assert ticket["prediction"]["sentiment"] == "negative"
    assert ticket["prediction"]["priority"] == "high"
    assert ticket["prediction"]["model_version"] == "baseline-v1"


def test_get_ticket_by_id(client: TestClient) -> None:
    ticket = create_ticket(client)

    response = client.get(f"/api/v1/tickets/{ticket['id']}")

    assert response.status_code == 200
    assert response.json()["id"] == ticket["id"]


def test_list_tickets(client: TestClient) -> None:
    create_ticket(client)

    response = client.get("/api/v1/tickets?limit=10&offset=0&priority=high")

    assert response.status_code == 200
    body = response.json()
    assert body["total"] == 1
    assert len(body["items"]) == 1


def test_update_ticket_status(client: TestClient) -> None:
    ticket = create_ticket(client)

    response = client.patch(
        f"/api/v1/tickets/{ticket['id']}/status",
        json={"status": "in_progress"},
    )

    assert response.status_code == 200
    assert response.json()["status"] == "in_progress"


def test_rerun_prediction(client: TestClient) -> None:
    ticket = create_ticket(client)

    response = client.post(f"/api/v1/tickets/{ticket['id']}/predict")

    assert response.status_code == 200
    assert response.json()["prediction"]["model_version"] == "baseline-v1"


def test_invalid_source_returns_validation_error(client: TestClient) -> None:
    response = client.post(
        "/api/v1/tickets",
        json={
            "subject": "Need help",
            "description": "I need help with my support request.",
            "source": "social_media",
        },
    )

    assert response.status_code == 422


def test_delete_ticket_soft_deletes_record(client: TestClient) -> None:
    ticket = create_ticket(client)

    delete_response = client.delete(f"/api/v1/tickets/{ticket['id']}")
    get_response = client.get(f"/api/v1/tickets/{ticket['id']}")

    assert delete_response.status_code == 204
    assert get_response.status_code == 404
