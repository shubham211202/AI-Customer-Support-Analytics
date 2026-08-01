from ..common import (
    DEVICES,
    DEVICE_OS,
    BROWSERS,
    TIME_REFERENCES,
)
"""
Knowledge Base - Account
"""

CATEGORY = {
    "name": "Account",

    "team": "Account Support Team",

    "priority": [
        "Low",
        "Medium"
    ],

    "sentiment": [
        "Neutral",
        "Negative"
    ],

    "subjects": [
        "Unable to update profile",
        "Account verification pending",
        "Change registered email",
        "Profile information incorrect",
        "Account settings not saving",
        "Phone number update failed",
        "Unable to verify account",
        "Business profile issue",
        "Organization details incorrect",
        "Account locked"
    ],

    "errors": [
        "Verification failed",
        "Profile update failed",
        "Permission denied",
        "Unexpected server error",
        "Validation failed"
    ],

    "devices": DEVICES,

"device_os": DEVICE_OS,

"browsers": BROWSERS,

"time_references": TIME_REFERENCES,

    "actions": [
        "logged out and logged back in",
        "updated my browser",
        "used another device",
        "cleared browser cache"
    ],

    "impacts": [
        "My profile is incomplete.",
        "My team cannot use account features.",
        "Business information is incorrect."
    ],

    "requests": [
        "Please update my account.",
        "Kindly verify my account.",
        "Please resolve this issue."
    ]
}