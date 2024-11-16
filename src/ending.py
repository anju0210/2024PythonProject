import pygame
from base_scene import BaseScene
from game_state import GameState


class HappyEnding(BaseScene):
    def __init__(self, screen, character_pos=None, ghost=None, item=None, start_ticks=None, remaining_time=None):
        super().__init__(screen, character_pos, ghost, item)

        self.background = pygame.image.load("../assets/images/happyEnd_background.png").convert()
        self.background = pygame.transform.scale(self.background, (1080, 720))

        self.replay_button = pygame.image.load("../assets/images/replay_button.png").convert_alpha()
        self.replay_button = pygame.transform.scale(self.replay_button, (240, 96))
        self.replay_button_rect = self.replay_button.get_rect()
        self.replay_button_rect.x = 74
        self.replay_button_rect.y = 67

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            return GameState.START, None, None, None
        return GameState.HAPPYENDING, None, None, None


    def draw(self, time):
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.replay_button, self.replay_button_rect)

class SadEnding(HappyEnding):
    def __init__(self, screen, character_pos=None, ghost=None, item=None, start_ticks=None, remaining_time=None):
        super().__init__(screen, character_pos, ghost, item)
        self.background = pygame.image.load("../assets/images/sadEnd_background.png").convert()
        self.background = pygame.transform.scale(self.background, (1080, 720))


    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            return GameState.START, None, None, None
        return GameState.SADENDING, None, None, None
    def draw(self, time):
        super().draw(time)

