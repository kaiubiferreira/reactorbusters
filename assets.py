import os
import sys

import pygame

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("Reactor Busters")
clock = pygame.time.Clock()
# factor = 0.6
# WIDTH, HEIGHT = int(1600 * factor), int(900 * factor)
info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h

QUESTION_VIDEO_WIDTH = int(WIDTH * 0.62)
QUESTION_VIDEO_HEIGHT = int(QUESTION_VIDEO_WIDTH * 0.72)

NUMBER_OF_QUESTIONS = 5


def get_resource_path():
    if hasattr(sys, '_MEIPASS'):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, "resources")


RESOURCES = get_resource_path()

MENU_BACKGROUND = os.path.join(RESOURCES, "menu-background.jpg")
STATUS_WIDTH, STATUS_HEIGHT = 0.1 * HEIGHT, 0.1 * HEIGHT
SQUARE_PADDING = int(0.01 * HEIGHT)
VIDEO_PADDING = int(0.05 * HEIGHT)
TITLE_WIDTH, TITLE_HEIGHT = QUESTION_VIDEO_WIDTH, int(0.05 * HEIGHT)
LABEL_WIDTH, LABEL_HEIGHT = int(WIDTH * 0.35), int(0.05 * HEIGHT)
LABEL_RADIUS = int(0.02 * HEIGHT)

CARD_WIDTH = int(0.115 * WIDTH)
CARD_HEIGHT = int(CARD_WIDTH * 1.5)

CARD_BORDER_RADIUS = int(0.02 * HEIGHT)
CARD_PADDING = int(0.01 * HEIGHT)
CARD_BORDER_WIDTH = int(0.01 * HEIGHT)

BUTTON_WIDTH, BUTTON_HEIGHT = 130, STATUS_HEIGHT
BUTTON_RADIUS = int(0.02 * HEIGHT)

RIGHT_IMAGE = pygame.image.load(os.path.join(RESOURCES, "right_answer.png"))
WRONG_IMAGE = pygame.image.load(os.path.join(RESOURCES, "wrong_answer.png"))

SUCCESS_IMAGE = pygame.image.load(os.path.join(RESOURCES, "success.png"))
FAILURE_IMAGE = pygame.image.load(os.path.join(RESOURCES, "failure.png"))

CREDITS_IMAGE = pygame.image.load(os.path.join(RESOURCES, "credits.png"))
INTRODUCTION_IMAGE = pygame.image.load(os.path.join(RESOURCES, "introduction.png"))
RULES_IMAGE = pygame.image.load(os.path.join(RESOURCES, "rules.png"))

PENDING_COLOR = (169, 169, 169)

QUESTIONS = {
    'question_1': {
        'question': 'France?',
        'video': 'question_1.mp4',
        'answer': [
            'adsorption_molecular',
            'reaction_single_site',
            'desorption_absent'
        ]
    },
    'question_2': {
        'question': 'What is the capital of Germany?',
        'video': 'question_1.mp4',
        'answer': [
            'adsorption_molecular',
            'reaction_single_site',
            'desorption_absent'
        ]
    },
    'question_3': {
        'question': 'What is the capital of Germany?',
        'video': 'question_1.mp4',
        'answer': [
            'adsorption_molecular',
            'reaction_single_site',
            'desorption_absent'
        ]
    },
    'question_4': {
        'question': 'What is the capital of Germany?',
        'video': 'question_1.mp4',
        'answer': [
            'adsorption_molecular',
            'reaction_single_site',
            'desorption_absent'
        ]
    },
    'question_5': {
        'question': 'What is the capital of Germany?',
        'video': 'question_1.mp4',
        'answer': [
            'adsorption_molecular',
            'reaction_single_site',
            'desorption_absent'
        ]
    },
    'question_6': {
        'question': 'What is the capital of Germany?',
        'video': 'question_1.mp4',
        'answer': [
            'adsorption_molecular',
            'reaction_single_site',
            'desorption_absent'
        ]
    },
    'question_7': {
        'question': 'What is the capital of Germany?',
        'video': 'question_1.mp4',
        'answer': [
            'adsorption_molecular',
            'reaction_single_site',
            'desorption_absent'
        ]
    }
}

CARDS = [
    {
        'id': 'adsorption_molecular',
        'title': 'Adsorção Molecular',
        'group': 'Adsorption',
        'image': pygame.image.load(os.path.join(RESOURCES, 'cards', 'adsorption_molecular.png'))
    },
    {
        'id': 'adsorption_dissociative',
        'title': 'Adsorção Dissociativa',
        'group': 'Adsorption',
        'image': pygame.image.load(os.path.join(RESOURCES, 'cards', 'adsorption_dissociative.png'))
    },
    {
        'id': 'reaction_single_site',
        'title': 'Reação Sítio Único',
        'group': 'Reaction',
        'image': pygame.image.load(os.path.join(RESOURCES, 'cards', 'reaction_single_site.png'))
    },
    {
        'id': 'reaction_eley_rideal',
        'title': 'Reação Eley - Rideal',
        'group': 'Reaction',
        'image': pygame.image.load(os.path.join(RESOURCES, 'cards', 'reaction_eley_rideal.png'))
    },
    {
        'id': 'reaction_double_site',
        'title': 'Reação Sítio Duplo',
        'group': 'Reaction',
        'image': pygame.image.load(os.path.join(RESOURCES, 'cards', 'reaction_double_site.png'))
    },
    {
        'id': 'reaction_double_site_same_site',
        'title': 'Reação Sítio Duplo Mesmo Sítio',
        'group': 'Reaction',
        'image': pygame.image.load(os.path.join(RESOURCES, 'cards', 'reaction_double_site_same_site.png'))
    },
    {
        'id': 'reaction_double_site_different_site',
        'title': 'Reação Sítio Duplo Sítio Diferente',
        'group': 'Reaction',
        'image': pygame.image.load(os.path.join(RESOURCES, 'cards', 'reaction_double_site_same_site.png'))
    },
    {
        'id': 'desorption',
        'title': 'Dessorção',
        'group': 'Desorption',
        'image': pygame.image.load(os.path.join(RESOURCES, 'cards', 'desorption.png'))
    },
    {
        'id': 'desorption_absent',
        'title': 'Dessorção ausente',
        'group': 'Desorption',
        'image': pygame.image.load(os.path.join(RESOURCES, 'cards', 'desorption_absent.png'))
    }
]
