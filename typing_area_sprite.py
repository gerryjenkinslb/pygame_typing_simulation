# DirtySprite Class version to support simulating human typing
# in an area in PyGame with Scrolling (known as typwriter effect)
# Inter-key timing is random based inspired by this paper:
#    Dhakal, V., Feit, A., Kristensson, P.O. and Oulasvirta, A. 2018.
#    'Observations on typing from 136 million keystrokes.'
#    In Proceedings of the 36th ACM Conference on Human
#    Factors in Computing Systems (CHI 2018). ACM Press.


import pygame
import time
from random import gauss
from collections import deque
import os

# 40 WPM (Words per min)  converted to CPS (chars per second)
CPS_40WPM = 5 * 40 / 60
BASE_DELAY_MS = 1000/CPS_40WPM  # default time between chars in ms for 40 WPM


def _type_delay(word_per_min=40.0):  # set speed as words per minute
    """Returns a random millisecond delay value that is based on a
    normal random curve of a person typing at the
    optional parameter value Words Per Minute
    """

    # Humans max typing record is about 215
    #  Average is 35, To get a job typing, you need 60 to 80 WPM

    speed_factor = 40/word_per_min
    mean = BASE_DELAY_MS * speed_factor   # adjust the mean time

    v = gauss(mean, mean/2)  # random time between chars to normal curve
    return min(max(0.0, v), 3000.0 * speed_factor)  # max delay is 3000 ms


class TypingAreaSprite(pygame.sprite.DirtySprite):
    """Class to automate a dirty sprite area that text is typed into in PyGame.

    see testit method at end of this file for sample of use.

    Note: you can dynamically add to char queue by using either:
       obj.char_queue.extend(string) or obj.char_queue.append(char)
    """

    def __init__(self, text, area, font, fg_color, bk_color, wps=80):
        """
        Constructor Args:
            text: text to display
            area: PyGame Rect Object specifying the screen rectangle
            font, fg_color, bk_color: font specs
            wps: an optional parameter to set the speed of typing, 80 wps default
        """
        pygame.sprite.DirtySprite.__init__(self)
        self.char_queue = deque(text)  # used for queue of text to display
        self.rect = area.copy()
        self.font = font
        self.fg_color = fg_color
        self.bk_color = bk_color

        self.size = area.size
        self.image = pygame.Surface(self.size, flags=pygame.SRCALPHA)
        self.image.fill(bk_color)  # clear typing area

        self.wps = wps
        self.y = 0  # keep track of vertical position of next line of text
        self.y_delta = self.font.size("M")[1]  # get height of line from a char

        self.line = ""  # current string buffer being rendered on line
        self.next_time = time.time()  # trigger time for next action
        self.dirty = 0  # set to signal draw method to copy to screen

    def _render_new_line(self):  # advance down or scroll up on '\n'
        self.y += self.y_delta  # advance position down in area
        self.line = ""  # reset line buffer
        if self.y + self.y_delta > self.size[1]:  # space for new line?
            # no, scroll area up
            self.image.blit(self.image, (0, -self.y_delta))
            self.y += -self.y_delta  # backup a line
            # erase bottom line
            pygame.draw.rect(self.image, self.bk_color,
                             (0, self.y, self.size[0], self.size[1] - self.y))
            self.dirty = 1

    def _render_char(self, c):  # render next char
        if c == '\n':
            self._render_new_line()
        else:
            self.line += c  # add new character to line buffer
            text = self.font.render(self.line, True, self.fg_color)
            self.image.blit(text, (0, self.y))  # render line
            self.dirty = 1

    def update(self):
        """Call obj.update() from pygame main game loop"""
        while self.char_queue and self.next_time <= time.time():  # time for char?
            self._render_char(self.char_queue.popleft())  # render it
            self.next_time += _type_delay(self.wps)/1000.0
        self.next_time = time.time()  # always reset to current tick time when waiting for char


    # call draw from pygame main loop after update
    def draw(self, screen):
        """Call obj.draw() from the main game loop"""

        if self.dirty:
            screen.blit(self.image, self.rect)  # transfer to screen
            self.dirty = 0


def testit():
    STORY = """
    Hello fellow programmers
    We endeavor to type code in precise
    ways and sometimes go down a rabbit
    hole of bits and bytes.

    Debugging our way through to a better
    understanding.. but it seems that we
    dwell forever in the error realms.

    We hope the bug will be revealed
    never to infest us again."""

    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)

    os.environ['SDL_VIDEO_WINDOW_POS'] = "300,450"
    pygame.init()
    w = 1100
    h = 420
    screen = pygame.display.set_mode((w, h))
    clock = pygame.time.Clock()

    # Create The Backgound
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((0, 0, 0))

    font = pygame.font.SysFont("Liberation Sans", 50)

    area_rect = pygame.Rect(25, 0, w - 50, h - 25)
    message = TypingAreaSprite(STORY, area_rect, font, WHITE, BLACK, wps=800)
    allsprites = pygame.sprite.LayeredDirty(message)

    allsprites.clear(screen, background)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        else:
            allsprites.update()

            # Draw Everything
            rects = allsprites.draw(screen)
            pygame.display.update(rects)
            clock.tick(60)

if __name__ == "__main__":
    testit()
