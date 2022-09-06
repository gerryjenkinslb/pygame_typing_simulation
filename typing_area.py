# Class to support simulating human typing in an area
# in PyGame with Scrolling (known as typwriter effect)
# Inter-key timing is random based inspired by this paper:
#    Dhakal, V., Feit, A., Kristensson, P.O. and Oulasvirta, A. 2018.
#    'Observations on typing from 136 million keystrokes.'
#    In Proceedings of the 36th ACM Conference on Human
#    Factors in Computing Systems (CHI 2018). ACM Press.


import pygame
import time
from random import gauss
from collections import deque

CPS_40WPM = 5 * 40 / 60  # 40 WPM (Words per min)  converted to CPS (chars per second)
BASE_DELAY_MS = 1000/CPS_40WPM  # default time between chars in ms for 40 WPM


def _type_delay(word_per_min=40.0):  # set speed as words per minute
    """Returns a random millisecond delay value that is based on a normal random curve
    of a person typing at the optional parameter value Words Per Minute
    """

    # Humans max typing record is about 215
    #  Average is 35, To get a job typing, you need 60 to 80 WPM

    speed_factor = 40/word_per_min
    mean = BASE_DELAY_MS * speed_factor   # adjust the mean time based on user multiplier

    v = gauss(mean, mean/2)  # create random delay in milliseconds
    return min(max(0.0, v), 3000.0 * speed_factor)  # max delay is 3 sec


class TypingArea:
    """Class to automate a rectangular area that text is typed into in PyGame. You can easily covert this
    class to a Sprite if needed

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

        self.text_buffer = deque(text)  # create deque of chars to output
        self.source_rect = area.copy()  # save area
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
                    self.next_time = time.time() + delay/1000.0
                else:
                    self.next_time = 0  # empty buffer, nothing to do
                self.update()  # do it again to catch more than one char event per tick

    # call draw from pygame main loop after update
    def draw(self, screen):
        """Call obj.draw() from the main game loop"""
        if self.dirty:
            screen.blit(self.image, self.source_rect)  # transfer to screen
            self.dirty = 0
