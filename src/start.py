import pygame
import math
from base_scene import BaseScene
from game_state import GameState


class Start(BaseScene):
    def __init__(self, screen, character_pos=None, ghost=None, item=None, start_ticks=None, remaining_time=None):
        super().__init__(screen, character_pos, ghost, item)

        self.background = pygame.image.load("../assets/images/start_background.png").convert()
        self.background = pygame.transform.scale(self.background, (1080, 720))

        self.title = pygame.image.load("../assets/images/title.png").convert_alpha()
        self.title = pygame.transform.scale(self.title, (616, 440))
        self.title_rect = self.title.get_rect()
        self.title_rect.centerx = self.screen.get_rect().centerx
        self.title_rect.y = 79

        self.start_button = pygame.image.load("../assets/images/start_button.png").convert_alpha()
        self.start_button = pygame.transform.scale(self.start_button, (184, 72))
        self.start_button_rect = self.start_button.get_rect()
        self.start_button_rect.x = 448
        self.start_button_rect.y = 545

        self.animation_time = 0
        self.original_y = float(self.title_rect.y)
        self.animation_speed = 1
        self.animation_range = 15

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            return GameState.TUTORIAL, None, None, None
        return GameState.START, None, None, None

    def update(self):
        self.animation_time += 0.02
        offset = math.sin(self.animation_time) * self.animation_range
        self.title_rect.y = self.original_y + offset

    def draw(self, time):
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.title, self.title_rect)
        self.screen.blit(self.start_button, self.start_button_rect)

