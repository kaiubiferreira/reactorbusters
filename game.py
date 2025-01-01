import random
import sys

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
    start_x = SQUARE_PADDING
    start_y = 0.87 * HEIGHT

    image_width = STATUS_WIDTH
    image_height = STATUS_HEIGHT

    right_image_resized = pygame.transform.scale(RIGHT_IMAGE, (image_width, image_height))
    wrong_image_resized = pygame.transform.scale(WRONG_IMAGE, (image_width, image_height))

    for i, state in enumerate(answers_state):
        if state == 'pending':
            pygame.draw.rect(screen, PENDING_COLOR,
                             (start_x + i * (image_width + SQUARE_PADDING), start_y,
                              image_width, image_height), border_radius=CARD_BORDER_RADIUS)
        elif state == 'right':
            screen.blit(right_image_resized, (start_x + i * (image_width + SQUARE_PADDING), start_y))
        elif state == 'wrong':
            screen.blit(wrong_image_resized, (start_x + i * (image_width + SQUARE_PADDING), start_y))


def draw_title(screen):
    y = 0.01 * HEIGHT
    x = WIDTH * 0.315 - (TITLE_WIDTH // 2)

    pygame.draw.rect(screen, COLORS['primary'], (x, y, TITLE_WIDTH, TITLE_HEIGHT), border_radius=LABEL_RADIUS)
    font = pygame.font.Font(None, 28)  # TODO: config
    text = 'Mecanismo de Reação'
    text_surface = font.render(text, True, COLORS['primary_text'])

    text_rect = text_surface.get_rect()

    # Position the text in the center of the rectangle
    text_rect.center = (x + TITLE_WIDTH // 2, y + TITLE_HEIGHT // 2)
    screen.blit(text_surface, text_rect)


def draw_label(screen):
    y = 0.01 * HEIGHT
    x = 0.81 * WIDTH - (LABEL_WIDTH // 2)
    pygame.draw.rect(screen, COLORS['primary'], (x, y, LABEL_WIDTH, LABEL_HEIGHT), border_radius=LABEL_RADIUS)
    font = pygame.font.Font(None, 28)  # TODO: config
    text = 'Escolha suas cartas'
    text_surface = font.render(text, True, COLORS['primary_text'])
    text_rect = text_surface.get_rect()
    text_rect.center = (x + LABEL_WIDTH // 2, y + LABEL_HEIGHT // 2)
    screen.blit(text_surface, text_rect)


def draw_cards(screen):
    # Constants for card layout
    cards_per_row = 3
    rows = 3

    # Base coordinates for positioning
    card_y = 0.06 * HEIGHT

    middle_x = 0.81 * WIDTH
    middles = [middle_x - CARD_WIDTH - CARD_PADDING, middle_x, middle_x + CARD_WIDTH + CARD_PADDING]

    # Loop through rows and columns to draw cards
    for row in range(rows):
        for col in range(cards_per_row):
            index = row * cards_per_row + col
            if index >= len(CARDS):
                break

            card = CARDS[index]
            card_x = middles[col] - CARD_WIDTH // 2
            rect = pygame.Rect(card_x, card_y, CARD_WIDTH, CARD_HEIGHT)
            card_positions[card['id']] = rect

            mouse_pos = pygame.mouse.get_pos()
            is_hover = rect.collidepoint(mouse_pos)
            is_selected = card['id'] in selected_cards
            card_image = pygame.transform.scale(card['image'], (CARD_WIDTH, CARD_HEIGHT))

            if is_selected:
                selected_rect = pygame.Rect(card_x - 5, card_y - 5, CARD_WIDTH + 10, CARD_HEIGHT + 10)
                border_rect = selected_rect.inflate(CARD_BORDER_WIDTH, CARD_BORDER_WIDTH)
                border_color = COLORS[card['group']]
                pygame.draw.rect(screen, border_color, border_rect)
                screen.blit(card_image, (card_x, card_y))
            elif is_hover:
                card_image = pygame.transform.scale(card['image'],
                                                    (CARD_WIDTH + CARD_BORDER_WIDTH, CARD_HEIGHT + CARD_BORDER_WIDTH))
                screen.blit(card_image, (card_x - CARD_BORDER_WIDTH // 2, card_y - CARD_BORDER_WIDTH // 2))
            else:
                screen.blit(card_image, (card_x, card_y))

        # Update card_y for the next row after drawing all cards in the current row
        card_y += CARD_HEIGHT + CARD_PADDING


def draw_buttons(screen):
    start_x = SQUARE_PADDING + (NUMBER_OF_QUESTIONS + 1) * (STATUS_WIDTH + SQUARE_PADDING)
    button_y = 0.87 * HEIGHT

    buttons = ['Voltar', 'Dicas', 'Confirmar']

    for button_index, button in enumerate(buttons):
        button_x = start_x + button_index * (BUTTON_WIDTH + SQUARE_PADDING)

        rect = pygame.Rect(button_x, button_y, BUTTON_WIDTH, BUTTON_HEIGHT)
        button_positions[button] = rect

        mouse_pos = pygame.mouse.get_pos()
        is_hover = rect.collidepoint(mouse_pos)

        active = button != 'Confirmar' or len(selected_cards) == 3

        if not active:
            button_color = COLORS['button_disabled']
        elif is_hover:
            button_color = COLORS['button_hover']
        else:
            button_color = COLORS['primary']

        pygame.draw.rect(screen, button_color, rect, border_radius=BUTTON_RADIUS)
        font = pygame.font.Font(None, 36)
        text_surface = font.render(button, True, COLORS['primary_text'])
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

    if index == 'Confirmar' and len(selected_cards) == 3:
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
        x = WIDTH * 0.315 - (TITLE_WIDTH // 2)
        y = 0.06 * HEIGHT

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
        draw_buttons(screen)
        pygame.display.flip()
        if exit_condition():
            break

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
