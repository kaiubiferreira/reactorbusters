import threading

from moviepy import VideoFileClip

from assets import *
from theme import COLORS

button_x = WIDTH * 0.5 - BUTTON_WIDTH // 2
button_y = HEIGHT * 0.9
rect = pygame.Rect(button_x, button_y, BUTTON_WIDTH, BUTTON_HEIGHT)

hover_cursor = pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_HAND)
default_cursor = pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_ARROW)
video_status = 'pending'


def play_video(video_path):
    global video_status
    clip = VideoFileClip(video_path)
    for frame in clip.iter_frames(fps=60, dtype='uint8'):
        frame_surface = pygame.surfarray.make_surface(frame)
        frame_surface = pygame.transform.flip(frame_surface, False, True)
        frame_surface = pygame.transform.rotate(frame_surface, 270)
        frame_surface = pygame.transform.scale(frame_surface, (WIDTH, HEIGHT))
        x = 0
        y = 0

        if video_status != 'running':
            break
        screen.blit(frame_surface, (x, y))


def clean_screen():
    background = pygame.image.load(GAME_BACKGROUND)
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))
    screen.blit(background, (0, 0))


def basic_video_screen(video, screen, clock):
    global video_status
    clean_screen()
    video_thread = threading.Thread(target=play_video, args=(video,))
    video_thread.start()
    video_status = 'running'
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = event.pos
                if rect.collidepoint(mouse_pos):
                    video_status = 'pending'
                    return

        pygame.mouse.set_cursor(default_cursor)

        mouse_pos = pygame.mouse.get_pos()
        is_hover = rect.collidepoint(mouse_pos)

        if is_hover:
            button_color = COLORS['button_hover']
            pygame.mouse.set_cursor(hover_cursor)
        else:
            button_color = COLORS['primary']

        pygame.draw.rect(screen, button_color, rect, border_radius=BUTTON_RADIUS)
        font = pygame.font.Font(None, 36)
        text_surface = font.render("Voltar", True, COLORS['primary_text'])
        text_rect = text_surface.get_rect(center=rect.center)
        screen.blit(text_surface, text_rect)

        pygame.display.flip()

        clock.tick(60)
