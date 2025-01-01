from assets import *
from basic_image_screen import basic_image_screen


def results_screen(resultado, screen, clock):
    if resultado > 3:
        image = SUCCESS_IMAGE
    else:
        image = FAILURE_IMAGE
    return basic_image_screen(image, screen, clock)
