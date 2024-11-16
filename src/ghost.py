import pygame
import random
import time
import math

class Ghost:
    def __init__(self, screen_width, screen_height, player):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.player = player

        self.image = pygame.image.load("../assets/images/ghost.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = 30
        self.rect.y = 30

        self.speed = 5
        self.start_time = time.time()
        self.appear_time = self.start_time + random.uniform(30, 100)
        self.is_visible = False


    def update(self):
        current_time = time.time()

        if not self.is_visible and current_time >= self.appear_time:
            self.is_visible = True
        if self.is_visible:
            self.follow_player()

    def follow_player(self):
        offset_distance = 60
        dx = self.player.x - self.rect.x
        dy = self.player.y - self.rect.y
        distance = math.hypot(dx, dy)

        if distance > offset_distance:
            dx, dy = dx / distance, dy / distance
            self.rect.x += dx * self.speed
            self.rect.y += dy * self.speed

    def draw(self, screen):
        if self.is_visible:
            screen.blit(self.image, (self.rect.x, self.rect.y))
