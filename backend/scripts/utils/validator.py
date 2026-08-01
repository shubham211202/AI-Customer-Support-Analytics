"""
Dataset Validator
"""


class TicketValidator:

    REQUIRED_FIELDS = [

        "ticket_id",

        "customer_name",

        "customer_email",

        "subject",

        "description",

        "category",

        "priority",

        "sentiment",

        "assigned_team"

    ]

    @classmethod
    def validate(cls, ticket):

        for field in cls.REQUIRED_FIELDS:

            if field not in ticket:

                return False

            if ticket[field] is None:

                return False

            if ticket[field] == "":

                return False

        return True