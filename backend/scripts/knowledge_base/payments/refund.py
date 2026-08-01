from ..common import (
    DEVICES,
    DEVICE_OS,
    BROWSERS,
    TIME_REFERENCES,
)
"""
Knowledge Base - Refund
"""

CATEGORY = {
    "name": "Refund",

    "team": "Billing Team",

    "priority": [
        "Medium",
        "High"
    ],

    "sentiment": [
        "Negative"
    ],

    "subjects": [
        "Refund not received",
        "Refund taking too long",
        "Duplicate payment refund",
        "Refund rejected",
        "Request refund",
        "Refund status unavailable",
        "Partial refund received",
        "Refund processing failed",
        "Cancelled order refund",
        "Refund confirmation missing"
    ],

    "errors": [
        "Refund service unavailable",
        "Refund processing failed",
        "Payment verification failed",
        "Unexpected server error"
    ],

    "devices": DEVICES,

"device_os": DEVICE_OS,

"browsers": BROWSERS,

"time_references": TIME_REFERENCES,

    "actions": [
        "checked my bank statement",
        "contacted customer support",
        "verified my payment details"
    ],

    "impacts": [
        "My funds are still unavailable.",
        "This is affecting my business expenses.",
        "The payment has not been returned."
    ],

    "requests": [
        "Please process my refund.",
        "Kindly investigate this issue.",
        "Please update me on the refund status."
    ]
}