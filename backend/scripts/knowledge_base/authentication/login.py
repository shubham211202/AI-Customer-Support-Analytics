from ..common import (
    DEVICES,
    DEVICE_OS,
    BROWSERS,
    TIME_REFERENCES,
)

"""
AI Customer Support Analytics Platform

Knowledge Base - Login
"""

CATEGORY = {
    "name": "Login",

    "team": "Authentication Team",

    "priority": [
        "Medium",
        "High"
    ],

    "sentiment": [
        "Negative"
    ],

    "subjects": [
        "Unable to login",
        "Login failed",
        "Authentication error",
        "Cannot sign in",
        "Login page not responding",
        "Account locked after multiple attempts",
        "Two-factor authentication failed",
        "Unexpected logout after login",
        "Login stuck on loading screen",
        "Unable to access dashboard"
    ],

    "errors": [
        "Authentication failed",
        "Invalid credentials",
        "Access denied",
        "Session expired",
        "Internal server error",
        "Connection timeout",
        "Unexpected server error"
    ],

    "devices": DEVICES,

"device_os": DEVICE_OS,

"browsers": BROWSERS,

"time_references": TIME_REFERENCES,

    "actions": [
        "cleared browser cache",
        "restarted the application",
        "reinstalled the application",
        "reset my password",
        "tried another browser",
        "used another device",
        "disabled VPN"
    ],

    "impacts": [
        "I cannot continue my work.",
        "My business operations are affected.",
        "My support team is blocked.",
        "Customers are waiting for a response.",
        "This issue is impacting productivity."
    ],

    "requests": [
        "Please investigate this issue.",
        "Kindly resolve this as soon as possible.",
        "Looking forward to your assistance.",
        "Please provide a solution."
    ]
}