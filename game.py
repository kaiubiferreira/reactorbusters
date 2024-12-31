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
    # Adjust to place squares vertically
    start_x = (WIDTH // 32) * 29.5
    start_y = TOP_MARGIN + TITLE_HEIGHT + SQUARE_PADDING

    colors = {
        'pending': (169, 169, 169),  # Gray
        'right': (0, 255, 0),  # Green
        'wrong': (255, 0, 0)  # Red
    }

    for i, state in enumerate(answers_state):
        color = colors[state]
        pygame.draw.rect(screen, color,
                         (start_x, start_y + i * (STATUS_RECT_HEIGHT + SQUARE_PADDING), STATUS_RECT_WIDTH,
                          STATUS_RECT_HEIGHT))


def draw_title(screen):
    y = TOP_MARGIN
    x = (WIDTH / 2 - TITLE_WIDTH) // 2
    pygame.draw.rect(screen, COLORS['primary'], (x, y, TITLE_WIDTH, TITLE_HEIGHT), border_radius=LABEL_RADIUS)
    font = pygame.font.Font(None, 28)  # TODO: config
    text = 'Mecanismo de Reação'
    text_surface = font.render(text, True, COLORS['primary_text'])

    text_rect = text_surface.get_rect()

    # Position the text in the center of the rectangle
    text_rect.center = (x + TITLE_WIDTH // 2, y + TITLE_HEIGHT // 2)
    screen.blit(text_surface, text_rect)


def draw_label(screen):
    y = TOP_MARGIN
    x = WIDTH // 2 + WIDTH // 4 - LABEL_WIDTH // 2 - 50
    pygame.draw.rect(screen, COLORS['primary'], (x, y, LABEL_WIDTH, LABEL_HEIGHT), border_radius=LABEL_RADIUS)
    font = pygame.font.Font(None, 28)  # TODO: config
    text = 'Escolha suas cartas'
    text_surface = font.render(text, True, COLORS['primary_text'])

    text_rect = text_surface.get_rect()

    # Position the text in the center of the rectangle
    text_rect.center = (x + LABEL_WIDTH // 2, y + LABEL_HEIGHT // 2)
    screen.blit(text_surface, text_rect)


def draw_cards(screen):
    # Constants for card layout
    cards_per_row = 3
    rows = 3

    # Base coordinates for positioning
    card_width_with_padding = CARD_WIDTH + CARD_PADDING
    card_y = TOP_MARGIN + CARD_PADDING + TITLE_HEIGHT

    # Loop through rows and columns to draw cards
    for row in range(rows):
        for col in range(cards_per_row):
            index = row * cards_per_row + col
            if index >= len(CARDS):
                break

            card = CARDS[index]
            card_x = (WIDTH // 2 + WIDTH // 4 - 50) - (cards_per_row * CARD_WIDTH + (
                    cards_per_row - 1) * CARD_PADDING) // 2 + col * card_width_with_padding
            rect = pygame.Rect(card_x, card_y, CARD_WIDTH, CARD_HEIGHT)
            card_positions[card['id']] = rect

            mouse_pos = pygame.mouse.get_pos()
            is_hover = rect.collidepoint(mouse_pos)
            is_selected = card['id'] in selected_cards

            if is_hover or is_selected:
                hover_rect = pygame.Rect(card_x - 5, card_y - 5, CARD_WIDTH + 10, CARD_HEIGHT + 10)
                if is_selected:
                    border_rect = hover_rect.inflate(CARD_BORDER_WIDTH,
                                                     CARD_BORDER_WIDTH)  # Inflate the rect for border
                    border_color = COLORS[card['group']]
                    pygame.draw.rect(screen, border_color, border_rect, border_radius=CARD_BORDER_RADIUS)
                pygame.draw.rect(screen, (120, 120, 0), hover_rect, border_radius=CARD_BORDER_RADIUS)
            else:
                pygame.draw.rect(screen, (120, 120, 0), rect, border_radius=CARD_BORDER_RADIUS)

            # Blit the image onto the card
            # screen.blit(images[i], (card_x + CARD_PADDING, card_y + CARD_PADDING))

        # Update card_y for the next row after drawing all cards in the current row
        card_y += CARD_HEIGHT + CARD_PADDING


def draw_confirm_button(screen):
    start_y = TOP_MARGIN + TITLE_HEIGHT + SQUARE_PADDING + 50
    button_x = (WIDTH // 32) * 30.5 - CONFIRM_BUTTON_WIDTH // 2
    button_y = start_y + NUMBER_OF_QUESTIONS * (STATUS_RECT_HEIGHT + SQUARE_PADDING)

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


def get_card_by_id(identity):
    for card in CARDS:
        if card['id'] == identity:
            return card

    return None


def click_card(index):

    print(f'index: {index}')
    clicked_card = get_card_by_id(index)
    print(f'clicked_card: {clicked_card}')

    for card_index in selected_cards:
        card = get_card_by_id(card_index)
        if card['group'] == clicked_card['group']:
            selected_cards.remove(card_index)

    selected_cards.append(index)
    print(f'selected_cards: {selected_cards}')


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
        x = (WIDTH // 2 - QUESTION_VIDEO_WIDTH) // 2
        y = 20 + TITLE_HEIGHT

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Check for mouse button click
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = event.pos
                for identity, pos in card_positions.items():
                    if pos.collidepoint(mouse_pos):
                        click_card(identity)
                for identity, pos in button_positions.items():
                    if pos.collidepoint(mouse_pos):
                        click_button(identity)

        screen.fill((255, 255, 255))
        card_positions.clear()
        screen.blit(frame_surface, (x, y))
        draw_status_bar(screen)
        draw_title(screen)
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
