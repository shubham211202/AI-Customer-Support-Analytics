"""
Description Generator
"""

import random

from knowledge_base import KNOWLEDGE_BASE

from generators.template_engine import TemplateEngine
from generators.personality_engine import PersonalityEngine
from generators.context_engine import ContextEngine


class DescriptionGenerator:

    def __init__(self):
        self.template_engine = TemplateEngine()
        self.personality_engine = PersonalityEngine()
        self.context_engine = ContextEngine()

    def generate(self, category: str) -> str:
        kb = KNOWLEDGE_BASE[category]

        # Get personality
        _, personality = self.personality_engine.get_personality()

        # Get context
        context = self.context_engine.get_context()

        # Device information
        device = random.choice(kb["devices"])
        operating_system = random.choice(
            kb["device_os"][device]
        )
        browser = random.choice(kb["browsers"])

        # Get template
        template = self.template_engine.get_template()

        # Generate description
        description = template.format(
            intro=random.choice(personality["intros"]),

            problem=(
                f"{context}, I tried to access my account using "
                f"{browser} on my {device} running "
                f"{operating_system}. "
                f"The system displays "
                f"'{random.choice(kb['errors'])}'."
            ),

            attempt=(
                f"I already {random.choice(kb['actions'])}, "
                f"but the issue still persists."
            ),

            impact=random.choice(kb["impacts"]),

            request=random.choice(personality["requests"]),

            emotion=random.choice([
                "I'm really frustrated.",
                "This is becoming difficult.",
                "I'm worried about this issue.",
                "This problem is affecting my work."
            ]),

            device_info=(
                f"I am using {device} running "
                f"{operating_system} with {browser}."
            )
        )

        return description