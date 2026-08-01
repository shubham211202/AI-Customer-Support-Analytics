from ..common import (
    DEVICES,
    DEVICE_OS,
    BROWSERS,
    TIME_REFERENCES,
)
"""
Knowledge Base - Password Reset
"""

CATEGORY = {
    "name": "Password Reset",

    "team": "Authentication Team",

    "priority": [
        "Low",
        "Medium"
    ],

    "sentiment": [
        "Neutral",
        "Negative"
    ],

    "subjects": [
        "Password reset email not received",
        "Reset link expired",
        "Unable to reset password",
        "Forgot password issue",
        "Password reset page not working",
        "Reset code invalid",
        "Password change failed",
        "Temporary password not working",
        "Cannot create new password",
        "Password reset loop"
    ],

    "errors": [
        "Reset token expired",
        "Invalid reset token",
        "Verification failed",
        "OTP expired",
        "Email not recognized",
        "Unexpected server error"
    ],

    "devices": DEVICES,

"device_os": DEVICE_OS,

"browsers": BROWSERS,

"time_references": TIME_REFERENCES,

    "actions": [
        "requested another reset email",
        "checked my spam folder",
        "tried another browser",
        "used another device",
        "cleared browser cache"
    ],

    "impacts": [
        "I cannot access my account.",
        "My work is delayed.",
        "I cannot continue using the platform.",
        "My team cannot access shared resources."
    ],

    "requests": [
        "Please help me reset my password.",
        "Kindly investigate this issue.",
        "Please provide a working reset link.",
        "Looking forward to your assistance."
    ]
}