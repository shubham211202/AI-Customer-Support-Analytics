"""
Context Engine

Responsible for generating realistic situations
that occurred before the customer experienced the issue.
"""

import random

ACCOUNT_CONTEXTS = [
    "after changing my email address",
    "after updating my phone number",
    "after enabling two-factor authentication",
    "after modifying my account details",
]

DEVICE_CONTEXTS = [
    "after switching to a new phone",
    "after buying a new laptop",
    "after changing my browser",
    "after resetting my device",
]

APP_CONTEXTS = [
    "after updating the mobile application",
    "after installing the latest version",
    "after reinstalling the application",
]

LOGIN_CONTEXTS = [
    "after entering the wrong password several times",
    "after my session expired",
    "after logging in from another location",
]

NETWORK_CONTEXTS = [
    "while using office Wi-Fi",
    "while connected to mobile data",
    "while travelling abroad",
]


class ContextEngine:

    def __init__(self):
        self.contexts = (
            ACCOUNT_CONTEXTS
            + DEVICE_CONTEXTS
            + APP_CONTEXTS
            + LOGIN_CONTEXTS
            + NETWORK_CONTEXTS
        )

    def get_context(self) -> str:
        return random.choice(self.contexts)