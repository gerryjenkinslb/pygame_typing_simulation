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

CPS_40WPM = 5 * 40 / 60  # 40 WPM (Words per min)  converted to CPS (chars per second)
BASE_DELAY_MS = 1000 / CPS_40WPM  # default time between chars in ms for 40 WPM


def _type_delay(word_per_min=40.0):  # set speed as words per minute
    """Returns a random millisecond delay value that is based on a normal random curve
    of a person typing at the optional parameter value Words Per Minute
    """

    # Humans max typing record is about 215
    #  Average is 35
    #  To get a job typing, you need 60 to 80 WPM

    speed_factor = 40 / word_per_min
    mean = BASE_DELAY_MS * speed_factor  # adjust the mean time based on user multiplier

    v = gauss(mean, mean / 2)  # create random delay in milliseconds
    return min(max(0.0, v), 3000.0 * speed_factor)  # max delay is 3 sec


class TypingAreaSprite(pygame.sprite.DirtySprite):
    """Class to automate a dirty sprite area that text is typed into in PyGame.

    To use, just create object, and call the update and draw methods in the normal game loop
    """

    def __init__(self, text, area, font, fg_color, bk_color, word_per_min=80):  # speed relative faster or slower
        """Constructor call  TypingClass(text, area, fond, fg_color, bk_color, word_per_min=80)

        Args:
            text: string of test to display, can add more by using obj.text_buffer.extend(text)
            area: PyGame Rect Object specifying the screen rectangle
            font, fg_color, bk_color: font and its foreground and background color
            word_per_min: an optional parameter to set speed of typing
        """
        pygame.sprite.DirtySprite.__init__(self)
        self.text_buffer = deque(text)  # create deque of chars to output
        self.rect = area.copy()  # save area
        self.font = font
        self.fg_color = fg_color
        self.bk_color = bk_color

        self.size = area.size
        self.image = pygame.Surface(self.size, flags=pygame.SRCALPHA)
        self.image.fill(bk_color)

        self.wps = word_per_min
        self.y = 0  # keep track of vertical position of next line of text
        self.y_delta = self.font.size("M")[1]  # get Height of a Char for advancing line down or scrolling

        self.line = ""  # current string being rendered on line
        self.next_time = 0.0  # trigger time for next action
        self.dirty = 0  # set to signal draw method to copy to screen

    def _newline_line(self):  # handle action when a new line is encountered advance down or scroll up
        self.y += self.y_delta
        self.line = ""
        if self.y + self.y_delta > self.size[1]:  # line does not fit in remaining space
            self.image.blit(self.image, (0, -self.y_delta))  # scroll up
            self.y += -self.y_delta  # backup a line
            pygame.draw.rect(self.image, self.bk_color,
                             (0, self.y, self.size[0], self.size[1] - self.y))
            self.dirty = 1

    def _new_char(self, c):  # render next char
        if c == '\n':
            self._newline_line()
        else:
            self.line += c
            text = self.font.render(self.line, True, self.fg_color)
            self.image.blit(text, (0, self.y))
            self.dirty = 1

    def update(self):
        """Call obj.update() from pygame main game loop"""
        if self.text_buffer:  # char available
            if self.next_time < time.time():  # check if time to render next char
                self._new_char(self.text_buffer.popleft())  # pop char
                if self.text_buffer:  # if more chars, the setup next time
                    delay = _type_delay(self.wps)
                    self.next_time = time.time() + delay / 1000.0
                else:
                    self.next_time = 0  # empty buffer, nothing to do
                self.update()  # do it again to catch more than one char event per tick

    # call draw from pygame main loop after update
    def draw(self, screen):
        """Call obj.draw() from the main game loop"""
        if self.dirty:
            screen.blit(self.image, self.rect)  # transfer to screen
            self.dirty = 0

def testit():
    STORY = """Hello fellow programmers
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
    message = TypingAreaSprite(STORY, area_rect, font, WHITE, BLACK, word_per_min=800)
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
