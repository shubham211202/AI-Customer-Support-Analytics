"""
AI Customer Support Analytics Platform

Customer Generator

Generates realistic customer profiles.
"""

import random
from faker import Faker


class CustomerGenerator:
    """
    Generates synthetic customer information.
    """

    def __init__(self):

        self.fake = Faker()

        self.customer_types = [
            "Free",
            "Basic",
            "Premium",
            "Enterprise"
        ]

        self.countries = [
            "India",
            "USA",
            "Canada",
            "Germany",
            "United Kingdom",
            "Australia",
            "Singapore",
            "Japan",
            "Brazil",
            "UAE"
        ]

        self.channels = [
            "Email",
            "Phone",
            "Chat",
            "Website",
            "Mobile App"
        ]

        self.products = [
            "CRM Suite",
            "AI Analytics Platform",
            "Cloud Storage",
            "Payment Gateway",
            "Reporting Engine",
            "API Platform",
            "Mobile Application",
            "Web Dashboard"
        ]

    def generate(self):

        return {

            "customer_name": self.fake.name(),

            "customer_email": self.fake.unique.email(),

            "customer_type": random.choice(self.customer_types),

            "country": random.choice(self.countries),

            "channel": random.choice(self.channels),

            "product": random.choice(self.products)

        }