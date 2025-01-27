from assets import *
from basic_video_screen import basic_video_screen


def results_screen(resultado, screen, clock):
    if resultado >= 5:
        video = SUCCESS_VIDEO
    elif resultado >= 3:
        video = MEDIUM_SUCCESS_VIDEO
    else:
        video = FAILURE_VIDEO
    return basic_video_screen(video, screen, clock)
