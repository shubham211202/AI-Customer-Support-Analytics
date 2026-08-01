from ..common import (
    DEVICES,
    DEVICE_OS,
    BROWSERS,
    TIME_REFERENCES,
)
"""
Knowledge Base - Billing
"""

CATEGORY = {
    "name": "Billing",

    "team": "Billing Team",

    "priority": [
        "Medium",
        "High"
    ],

    "sentiment": [
        "Negative"
    ],

    "subjects": [
        "Payment failed",
        "Double charged",
        "Invoice missing",
        "Incorrect billing amount",
        "Credit card declined",
        "Payment not reflected",
        "Billing statement incorrect",
        "Tax calculation issue",
        "Automatic payment failed",
        "Unable to download invoice"
    ],

    "errors": [
        "Payment gateway timeout",
        "Card declined",
        "Transaction failed",
        "Invoice generation failed",
        "Billing service unavailable",
        "Unexpected payment error"
    ],

    "devices": DEVICES,

"device_os": DEVICE_OS,

"browsers": BROWSERS,

"time_references": TIME_REFERENCES,

    "actions": [
        "tried another payment method",
        "contacted my bank",
        "used another browser",
        "retried the payment",
        "cleared browser cache"
    ],

    "impacts": [
        "I cannot complete my purchase.",
        "Our subscription has been interrupted.",
        "Business operations are affected.",
        "Our finance team is waiting for this invoice."
    ],

    "requests": [
        "Please resolve the billing issue.",
        "Kindly investigate the payment failure.",
        "Please generate the invoice.",
        "Looking forward to your assistance."
    ]
}