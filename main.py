# PyGame simulate Human typing or the "Typewriter" effect

# We define a class called 'TypingArea' that implements a rectangular are that
# can display text onto it as if it was being typed by a human, this is called
# the Typewriter effect.
# In the code we need to handle the timing in pygame and when to advance a line
# or to scroll up if we have reached the end of the area we also handle the
# char by char display to simulate typing


# Note: Char per sec (CPS) = Words per min (WPM) * 5 * 60

import pygame
import os
from typing_area import TypingArea

# some colors defined
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREY = (200, 200, 200)


# Test this Class
STORY = """Hello fellow programmers
We endeavor to type code in precise
ways and sometimes go down a rabbit
hole of bits and bytes.

Debugging our way through to a better
understanding.. but it seems that we
dwell forever in the error realms.

We hope the bug will be revealed
never to infest us again."""


def example1():
    # start up pygame
    os.environ['SDL_VIDEO_WINDOW_POS'] = "350,550"

    pygame.init()
    w = 1100
    h = 420
    screen = pygame.display.set_mode((w, h))
    screen.fill((128, 128, 128))
    clock = pygame.time.Clock()

    font = pygame.font.SysFont("Liberation Sans", 40)

    area_rect = pygame.Rect(50, 50, w-100, h-100)
    message = TypingArea(STORY, area_rect, font, WHITE, BLACK, wps=400)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
        else:
            message.update()
            message.draw(screen)
            
            pygame.display.flip()
            clock.tick(60)


if __name__ == "__main__":
    example1()



