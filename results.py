from assets import *
from basic_video_screen import basic_video_screen


def results_screen(resultado, screen, clock):
    if resultado > 3:
        video = SUCCESS_IMAGE
    else:
        video = FAILURE_VIDEO
    return basic_video_screen(video, screen, clock)
