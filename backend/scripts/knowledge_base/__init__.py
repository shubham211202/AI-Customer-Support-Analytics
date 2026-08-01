from .authentication.login import CATEGORY as LOGIN
from .authentication.password_reset import CATEGORY as PASSWORD_RESET
from .authentication.account import CATEGORY as ACCOUNT
from .payments.billing import CATEGORY as BILLING
from .payments.subscription import CATEGORY as SUBSCRIPTION
from .payments.refund import CATEGORY as REFUND

KNOWLEDGE_BASE = {
    "Login": LOGIN,
    "Password Reset": PASSWORD_RESET,
    "Account": ACCOUNT,
    "Billing": BILLING,
    "Subscription": SUBSCRIPTION,
    "Refund": REFUND,
}