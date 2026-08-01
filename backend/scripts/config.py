"""
AI Customer Support Analytics Platform

Configuration
"""

# =====================================
# Dataset Configuration
# =====================================

NUM_TICKETS = 100000

RANDOM_SEED = 42

OUTPUT_FILE = "customer_support_dataset.csv"

# =====================================
# Ticket Status
# =====================================

STATUS = [
    "Open",
    "In Progress",
    "Resolved",
    "Closed"
]

# =====================================
# Customer Types
# =====================================

CUSTOMER_TYPES = [
    "Free",
    "Basic",
    "Premium",
    "Enterprise"
]

# =====================================
# Category Distribution
# (Must sum to 1.0)
# =====================================

CATEGORY_DISTRIBUTION = {

    "Technical": 0.18,

    "Billing": 0.12,

    "Login": 0.10,

    "Password Reset": 0.08,

    "Account": 0.08,

    "Subscription": 0.07,

    "Refund": 0.06,

    "Website": 0.06,

    "Mobile App": 0.05,

    "API": 0.05,

    "Bug Report": 0.05,

    "Feature Request": 0.04,

    "Order": 0.03,

    "Shipping": 0.02,

    "Returns": 0.01,

    "General Inquiry": 0.10

}