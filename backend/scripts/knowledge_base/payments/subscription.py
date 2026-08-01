from ..common import (
    DEVICES,
    DEVICE_OS,
    BROWSERS,
    TIME_REFERENCES,
)
"""
Knowledge Base - Subscription
"""

CATEGORY = {
    "name": "Subscription",

    "team": "Subscription Team",

    "priority": [
        "Medium"
    ],

    "sentiment": [
        "Neutral",
        "Negative"
    ],

    "subjects": [
        "Subscription not activated",
        "Unable to upgrade plan",
        "Subscription renewal failed",
        "Plan changed automatically",
        "Cancel subscription",
        "Downgrade request",
        "Trial expired unexpectedly",
        "Subscription missing",
        "Premium features unavailable",
        "Subscription invoice issue"
    ],

    "errors": [
        "Subscription service unavailable",
        "Renewal failed",
        "Plan activation failed",
        "Payment verification failed"
    ],

    "devices": DEVICES,

"device_os": DEVICE_OS,

"browsers": BROWSERS,

"time_references": TIME_REFERENCES,

    "actions": [
        "logged out and logged back in",
        "verified my payment",
        "used another browser"
    ],

    "impacts": [
        "Premium features are unavailable.",
        "My team cannot continue working.",
        "The subscription is inactive."
    ],

    "requests": [
        "Please activate my subscription.",
        "Kindly investigate the issue.",
        "Please restore my plan."
    ]
}