"""
Ticket Generator
"""

import random

from generators.customer_generator import CustomerGenerator
from generators.description_generator import DescriptionGenerator
from knowledge_base import KNOWLEDGE_BASE
from utils.helpers import generate_ticket_id


class TicketGenerator:

    def __init__(self):

        self.customer_generator = CustomerGenerator()
        self.description_generator = DescriptionGenerator()

    def generate_ticket(self):

        customer = self.customer_generator.generate()

        category = random.choice(list(KNOWLEDGE_BASE.keys()))

        kb = KNOWLEDGE_BASE[category]

        ticket = {

            **customer,

            "ticket_id": generate_ticket_id(),

            "subject": random.choice(kb["subjects"]),

            "description": self.description_generator.generate(category),

            "category": category,

            "priority": random.choice(kb["priority"]),

            "sentiment": random.choice(kb["sentiment"]),

            "assigned_team": kb["team"],

            "status": "Open"

        }

        return ticket