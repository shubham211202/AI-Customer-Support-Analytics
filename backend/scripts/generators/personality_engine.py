import random

PERSONALITIES = {
    "professional": {
        "intros": [
            "Hello Support Team,",
            "Dear Support,",
            "Good day,",
            "Hi Team,"
        ],

        "requests": [
            "Could you please investigate this issue?",
            "Kindly assist me with resolving this problem.",
            "I would appreciate your help.",
            "Looking forward to your response."
        ]
    },

    "calm": {
        "intros": [
            "Hi,",
            "Hello,",
            "Good morning,"
        ],

        "requests": [
            "Can someone help me?",
            "Please assist me.",
            "Thank you in advance."
        ]
    },

    "frustrated": {
        "intros": [
            "I'm really frustrated.",
            "I've already tried everything.",
            "This issue keeps happening."
        ],

        "requests": [
            "Please fix this soon.",
            "I need help immediately.",
            "This is affecting my work."
        ]
    },

    "angry": {
        "intros": [
            "This is unacceptable!",
            "I'm extremely disappointed.",
            "Why is this still happening?"
        ],

        "requests": [
            "Fix this immediately!",
            "I expect this to be resolved today.",
            "This level of service is unacceptable."
        ]
    },

    "confused": {
        "intros": [
            "I'm not sure what's happening.",
            "I think I made a mistake.",
            "Can someone explain this?"
        ],

        "requests": [
            "Please guide me.",
            "I'd appreciate some help.",
            "Thank you."
        ]
    }
}


class PersonalityEngine:

    def get_personality(self):
        personality = random.choice(list(PERSONALITIES.keys()))
        return personality, PERSONALITIES[personality]