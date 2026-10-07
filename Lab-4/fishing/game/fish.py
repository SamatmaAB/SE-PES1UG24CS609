"""
Fish: swims horizontally at a fixed depth, wrapping around when it
exits the screen. The starter has one fish type; Task 2 adds more.
"""

import pygame


SLOW_FISH_SPEED = 2
FAST_FISH_SPEED = 4
SLOW_POINTS = 10
FAST_POINTS = 20

SLOW_COLOR = (80, 180, 220)
FAST_COLOR = (220, 80, 80)


class Fish:
    def __init__(self, x, y, fish_type="slow", width=36, height=18):
        self.x = float(x)
        self.y = y
        if fish_type == "slow":
            self.speed = SLOW_FISH_SPEED
            self.point_value = SLOW_POINTS
            self.color = SLOW_COLOR
        else:
            self.speed = FAST_FISH_SPEED
            self.point_value = FAST_POINTS
            self.color = FAST_COLOR
        self.width = width
        self.height = height
        self.fish_type = fish_type

    def update(self, screen_width):
        self.x += self.speed
        if self.speed > 0 and self.x > screen_width:
            self.x = -self.width
        elif self.speed < 0 and self.x < -self.width:
            self.x = screen_width

    def get_rect(self):
        return pygame.Rect(
            int(self.x - self.width / 2), int(self.y - self.height / 2),
            self.width, self.height,
        )
