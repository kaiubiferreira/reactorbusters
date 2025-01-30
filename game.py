import random
import threading

from moviepy import VideoFileClip

from assets import *
from theme import COLORS

answers_state = ["pending" for q in range(NUMBER_OF_QUESTIONS)]
selected_questions = random.sample(list(QUESTIONS.keys()), NUMBER_OF_QUESTIONS)
card_positions = {}
button_positions = {}
selected_cards = []
current_question_index = 0
go_back = False
default_cursor = pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_ARROW)
hover_cursor = pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_HAND)
video_status = 'pending'


def reset():
    global answers_state, selected_questions, card_positions, button_positions, selected_cards, current_question_index, go_back, video_status
    pygame.mouse.set_cursor(default_cursor)
    answers_state = ["pending" for _ in range(NUMBER_OF_QUESTIONS)]
    selected_questions = random.sample(list(QUESTIONS.keys()), NUMBER_OF_QUESTIONS)
    card_positions = {}
    button_positions = {}
    selected_cards = []
    current_question_index = 0
    go_back = False
    video_status = 'pending'

    clean_screen()


def game_screen(screen, clock):
    reset()
    while True:
        pygame.mouse.set_cursor(default_cursor)
        check_click()
        show_question(screen, clock)
        card_positions.clear()
        draw_status_bar(screen)
        draw_title(screen)
        draw_label(screen)
        draw_cards(screen)
        draw_buttons(screen)
        pygame.display.flip()
        clock.tick(60)
        if exit_condition():
            return answers_state.count('right'), go_back


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
                pygame.mouse.set_cursor(hover_cursor)
            else:
                screen.blit(card_image, (card_x, card_y))

        # Update card_y for the next row after drawing all cards in the current row
        card_y += CARD_HEIGHT + CARD_PADDING


def draw_buttons(screen):
    start_x = SQUARE_PADDING + (NUMBER_OF_QUESTIONS + 1) * (STATUS_WIDTH + SQUARE_PADDING)
    button_y = 0.87 * HEIGHT

    buttons = ['Voltar', 'Confirmar']

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
            pygame.mouse.set_cursor(hover_cursor)
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


def clean_screen():
    background = pygame.image.load(GAME_BACKGROUND)
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))
    screen.blit(background, (0, 0))


def click_card(index):
    clean_screen()
    clicked_card = get_card_by_id(index)

    for card_index in selected_cards:
        card = get_card_by_id(card_index)
        if card['group'] == clicked_card['group']:
            selected_cards.remove(card_index)

    selected_cards.append(index)


def click_button(index):
    global current_question_index, go_back, video_status

    if index == 'Confirmar' and len(selected_cards) == 3:
        clean_screen()
        is_right = set(selected_cards) == set(QUESTIONS[selected_questions[current_question_index]]['answer'])
        answers_state[current_question_index] = 'right' if is_right else 'wrong'
        current_question_index = current_question_index + 1
        selected_cards.clear()
        video_status = 'reset'
    elif index == 'Voltar':
        go_back = True


def exit_condition():
    if current_question_index == NUMBER_OF_QUESTIONS or answers_state.count('wrong') >= 3 or go_back is True:
        return True


def check_click():
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


def play_video():
    global video_status
    question = QUESTIONS[selected_questions[current_question_index]]
    video = question['video']
    video_path = os.path.join(RESOURCES, video)
    clip = VideoFileClip(video_path)
    for frame in clip.iter_frames(fps=60, dtype='uint8'):
        frame_surface = pygame.surfarray.make_surface(frame)
        frame_surface = pygame.transform.flip(frame_surface, False, True)
        frame_surface = pygame.transform.rotate(frame_surface, 270)
        frame_surface = pygame.transform.scale(frame_surface, (QUESTION_VIDEO_WIDTH, QUESTION_VIDEO_HEIGHT))
        x = WIDTH * 0.315 - (TITLE_WIDTH // 2)
        y = 0.06 * HEIGHT
        clock.tick(60)


        screen.blit(frame_surface, (x, y))
        if exit_condition() or video_status == 'reset':
            break
    video_status = 'pending'


def show_question(screen, clock):
    global video_status

    if video_status == 'pending':
        video_status = 'running'
        video_thread = threading.Thread(target=play_video)
        video_thread.start()
