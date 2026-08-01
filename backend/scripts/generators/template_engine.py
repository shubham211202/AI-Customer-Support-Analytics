"""
Template Engine

Responsible for selecting a random description template.
"""

import random

TEMPLATES = [
    # Template 1
    "{intro}\n\n"
    "{problem}\n\n"
    "{request}",

    # Template 2
    "{intro}\n\n"
    "{problem}\n\n"
    "{impact}\n\n"
    "{request}",

    # Template 3
    "{intro}\n\n"
    "{problem}\n\n"
    "{attempt}\n\n"
    "{request}",

    # Template 4
    "{problem}",

    # Template 5
    "{intro}\n\n"
    "{problem}\n\n"
    "{emotion}\n\n"
    "{impact}\n\n"
    "{request}",

    # Template 6
    "{intro}\n\n"
    "{problem}\n\n"
    "{device_info}\n\n"
    "{request}",

    # Template 7
    "{problem}\n\n"
    "{attempt}\n\n"
    "{impact}",

    # Template 8
    "{intro}\n\n"
    "{problem}\n\n"
    "{attempt}\n\n"
    "{impact}\n\n"
    "{request}",
]


class TemplateEngine:
    """Returns a random description template."""

    def get_template(self) -> str:
        return random.choice(TEMPLATES)