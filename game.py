import random
import sys

import pygame
from moviepy import VideoFileClip

from assets import *
from theme import COLORS

answers_state = ["pending" for q in range(NUMBER_OF_QUESTIONS)]
selected_questions = random.sample(list(QUESTIONS.keys()), NUMBER_OF_QUESTIONS)
card_positions = {}
button_positions = {}
selected_cards = []
current_question_index = 0


def reset():
    global answers_state, selected_questions, card_positions, button_positions, selected_cards, current_question_index
    answers_state = ["pending" for q in range(NUMBER_OF_QUESTIONS)]
    selected_questions = random.sample(list(QUESTIONS.keys()), NUMBER_OF_QUESTIONS)
    card_positions = {}
    button_positions = {}
    selected_cards = []
    current_question_index = 0


def game_screen(screen, clock):
    reset()
    while True:
        show_question(screen)
        draw_status_bar(screen)
        pygame.display.flip()
        clock.tick(30)
        if exit_condition():
            return answers_state.count('right')


def draw_status_bar(screen):
    start_x = (WIDTH - STATUS_BAR_WIDTH) // 2
    start_y = QUESTION_VIDEO_HEIGHT - STATUS_RECT_HEIGHT + VIDEO_PADDING
    colors = {
        'pending': (169, 169, 169),  # Gray
        'right': (0, 255, 0),  # Green
        'wrong': (255, 0, 0)  # Red
    }

    for i, state in enumerate(answers_state):
        color = colors[state]
        pygame.draw.rect(screen, color,
                         (start_x + i * (STATUS_RECT_WIDTH + SQUARE_PADDING), start_y, STATUS_RECT_WIDTH,
                          STATUS_RECT_HEIGHT))


def draw_label(screen):
    y = QUESTION_VIDEO_HEIGHT + VIDEO_PADDING + STATUS_RECT_HEIGHT
    x = (WIDTH - STATUS_BAR_WIDTH) // 2
    pygame.draw.rect(screen, COLORS['primary'], (x, y, STATUS_BAR_WIDTH, STATUS_RECT_HEIGHT), border_radius=5)
    font = pygame.font.Font(None, 28)  # TODO: config
    text = 'Escolha suas cartas:'
    text_surface = font.render(text, True, COLORS['primary_text'])

    text_rect = text_surface.get_rect()

    # Position the text in the center of the rectangle
    text_rect.center = (x + STATUS_BAR_WIDTH // 2, y + STATUS_RECT_HEIGHT // 2)
    screen.blit(text_surface, text_rect)


def draw_cards(screen):
    # Draw cards
    card_y = QUESTION_VIDEO_HEIGHT + VIDEO_PADDING + STATUS_RECT_HEIGHT + STATUS_RECT_HEIGHT + SQUARE_PADDING
    card_x = (WIDTH - (7 * (CARD_WIDTH + CARD_PADDING))) // 2

    mouse_pos = pygame.mouse.get_pos()

    for card in CARDS:
        # Draw rounded rectangle for the card
        index = card['id']
        rect = pygame.Rect(card_x, card_y, CARD_WIDTH, CARD_HEIGHT)
        card_positions[index] = rect
        is_hover = rect.collidepoint(mouse_pos)
        is_selected = index in selected_cards
        if is_hover or is_selected:
            hover_rect = pygame.Rect(card_x - 5, card_y - 5, CARD_WIDTH + 10, CARD_HEIGHT + 10)
            if is_selected:
                border_rect = hover_rect.inflate(CARD_BORDER_WIDTH, CARD_BORDER_WIDTH)  # Inflate the rect for border
                border_color = COLORS[card['group']]
                pygame.draw.rect(screen, border_color, border_rect, border_radius=CARD_BORDER_RADIUS)
            pygame.draw.rect(screen, (120, 120, 0), hover_rect, border_radius=CARD_BORDER_RADIUS)
        else:
            pygame.draw.rect(screen, (120, 120, 0), rect, border_radius=CARD_BORDER_RADIUS)

        # Blit the image onto the card
        # screen.blit(images[i], (card_x + CARD_PADDING, card_y + CARD_PADDING))
        # Calculate the card position
        card_x = card_x + (CARD_WIDTH + CARD_PADDING)


def draw_confirm_button(screen):
    button_y = QUESTION_VIDEO_HEIGHT + VIDEO_PADDING + STATUS_RECT_HEIGHT + STATUS_RECT_HEIGHT + CARD_HEIGHT + \
               SQUARE_PADDING * 2
    button_x = (WIDTH - CONFIRM_BUTTON_WIDTH) // 2
    rect = pygame.Rect(button_x, button_y, CONFIRM_BUTTON_WIDTH, CONFIRM_BUTTON_HEIGHT)
    button_positions[f'confirm'] = rect

    mouse_pos = pygame.mouse.get_pos()
    is_hover = rect.collidepoint(mouse_pos)

    if len(selected_cards) < 3:
        button_color = COLORS['button_disabled']
    elif is_hover:
        button_color = COLORS['button_hover']
    else:
        button_color = COLORS['primary']

    pygame.draw.rect(screen, button_color, rect, border_radius=BUTTON_RADIUS)
    font = pygame.font.Font(None, 36)
    text_surface = font.render("Confirmar", True, COLORS['primary_text'])
    text_rect = text_surface.get_rect(center=rect.center)
    screen.blit(text_surface, text_rect)


def get_card_by_index(index):
    for card in CARDS:
        if card['id'] == index:
            return card

    return None


def click_card(index):
    clicked_card = get_card_by_index(index)

    for card_index in selected_cards:
        card = get_card_by_index(card_index)
        if card['group'] == clicked_card['group']:
            selected_cards.remove(card_index)

    selected_cards.append(index)


def click_button(index):
    global current_question_index

    if index == 'confirm' and len(selected_cards) == 3:
        is_right = set(selected_cards) == set(QUESTIONS[selected_questions[current_question_index]]['answer'])
        answers_state[current_question_index] = 'right' if is_right else 'wrong'
        current_question_index = current_question_index + 1
        selected_cards.clear()


def exit_condition():
    if current_question_index == NUMBER_OF_QUESTIONS or answers_state.count('wrong') >= 3:
        return True


def show_question(screen):
    question = QUESTIONS[selected_questions[current_question_index]]
    video = question['video']

    video_path = os.path.join("resources", video)
    clip = VideoFileClip(video_path)
    for frame in clip.iter_frames(fps=30, dtype='uint8'):
        frame_surface = pygame.surfarray.make_surface(frame)
        frame_surface = pygame.transform.flip(frame_surface, False, True)
        frame_surface = pygame.transform.rotate(frame_surface, 270)
        frame_surface = pygame.transform.scale(frame_surface, (QUESTION_VIDEO_WIDTH, QUESTION_VIDEO_HEIGHT))
        x = (WIDTH - QUESTION_VIDEO_WIDTH) // 2
        y = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Check for mouse button click
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = event.pos
                for index, pos in card_positions.items():
                    if pos.collidepoint(mouse_pos):
                        click_card(index)
                for index, pos in button_positions.items():
                    if pos.collidepoint(mouse_pos):
                        click_button(index)

        screen.fill((255, 255, 255))
        card_positions.clear()
        screen.blit(frame_surface, (x, y))
        draw_status_bar(screen)
        draw_label(screen)
        draw_cards(screen)
        draw_confirm_button(screen)
        pygame.display.flip()
        if exit_condition():
            break

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
