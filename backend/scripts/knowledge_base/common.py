"""
Common Knowledge Base

Shared values used across all ticket categories.
"""

# ----------------------------------
# Devices
# ----------------------------------

DEVICES = [
    "Windows Laptop",
    "MacBook Pro",
    "Linux Desktop",
    "Android Phone",
    "iPhone",
    "iPad"
]

# ----------------------------------
# Device → Operating System Mapping
# ----------------------------------

DEVICE_OS = {

    "Windows Laptop": [
        "Windows 10",
        "Windows 11"
    ],

    "MacBook Pro": [
        "macOS Sonoma",
        "macOS Sequoia"
    ],

    "Linux Desktop": [
        "Ubuntu 24.04",
        "Fedora 41"
    ],

    "Android Phone": [
        "Android 14",
        "Android 15"
    ],

    "iPhone": [
        "iOS 17",
        "iOS 18"
    ],

    "iPad": [
        "iPadOS 17",
        "iPadOS 18"
    ]
}

# ----------------------------------
# Browsers
# ----------------------------------

BROWSERS = [
    "Google Chrome",
    "Microsoft Edge",
    "Mozilla Firefox",
    "Safari"
]

# ----------------------------------
# Time References
# ----------------------------------

TIME_REFERENCES = [
    "today",
    "yesterday",
    "this morning",
    "last night",
    "two days ago",
    "last week"
]