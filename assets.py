import os

WIDTH, HEIGHT = 1600, 900

QUESTION_VIDEO_WIDTH, QUESTION_VIDEO_HEIGHT = 800, 800

NUMBER_OF_QUESTIONS = 5

MENU_BACKGROUND = os.path.join("resources", "menu-background.jpg")
STATUS_RECT_WIDTH, STATUS_RECT_HEIGHT = 100, 100
SQUARE_PADDING = 10
VIDEO_PADDING = 40
TITLE_WIDTH, TITLE_HEIGHT = 250, 50
LABEL_WIDTH, LABEL_HEIGHT = 250, 50
LABEL_RADIUS = 15
TOP_MARGIN = 10

CARD_WIDTH, CARD_HEIGHT = 256 * 0.7, 384 * 0.7
CARD_BORDER_RADIUS = 15
CARD_PADDING = 15
CARD_BORDER_WIDTH = 10

CONFIRM_BUTTON_WIDTH, CONFIRM_BUTTON_HEIGHT = 130, 50
BUTTON_RADIUS = 15

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
        'image': 'adsorption_molecular.png'
    },
    {
        'id': 'adsorption_dissociative',
        'title': 'Adsorção Dissociativa',
        'group': 'Adsorption',
        'image': 'adsorption_dissociative.png'
    },
    {
        'id': 'reaction_single_site',
        'title': 'Reação Sítio Único',
        'group': 'Reaction',
        'image': 'reaction_single_site.png'
    },
    {
        'id': 'reaction_double_site',
        'title': 'Reação Sítio Duplo',
        'group': 'Reaction',
        'image': 'reaction_double_site.png'
    },
    {
        'id': 'reaction_eley_rideal',
        'title': 'Reação Eley - Rideal',
        'group': 'Reaction',
        'image': 'reaction_eley_rideal.png'
    },
    {
        'id': 'desorption',
        'title': 'Dessorção',
        'group': 'Desorption',
        'image': 'desorption.png'
    },
    {
        'id': 'desorption_absent',
        'title': 'Dessorção ausente',
        'group': 'Desorption',
        'image': 'desorption_absent.png'
    },
    {
        'id': 'desorption_absent_2',
        'title': 'Dessorção ausente mesmo',
        'group': 'Desorption',
        'image': 'desorption_absent.png'
    },
    {
        'id': 'desorption_absent_3',
        'title': 'Dessorção bastante ausente',
        'group': 'Desorption',
        'image': 'desorption_absent.png'
    },
]
