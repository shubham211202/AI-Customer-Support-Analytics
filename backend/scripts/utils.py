import uuid


def generate_ticket_id():

    return f"TKT-{uuid.uuid4().hex[:10].upper()}"