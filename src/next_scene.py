import pygame
from game_state import GameState
from game import Game
from hedgehog import Hedgehog


class NextScene(Game):
    def __init__(self, screen, character_pos=None, ghost=None, item=None, start_ticks=None, remaining_time=None):
        super().__init__(screen, character_pos, ghost, item, start_ticks=None, remaining_time=None)
        self.font = pygame.font.Font("DungGeunMo.ttf", 24)

        self.background_image = pygame.image.load("../assets/images/nextgame_background.png").convert()
        self.background_image = pygame.transform.scale(self.background_image, (1080, 720))

        self.hedgehog1 = Hedgehog(300, 210)
        self.hedgehog2 = Hedgehog(500, 300)
        self.hedgehog3 = Hedgehog(700, 320)

    def handle_event(self, event):
        screen_transition = self.check_screen_transition(self.character_rect)
        if screen_transition:
            return screen_transition
        return GameState.PLAYING_NEXT, (0, self.character_rect.y), self.ghost, self.item


    def check_screen_transition(self, character_rect):
        if self.character_rect.x < -10:
            if self.ghost:
                self.ghost.rect.x = (self.screen_width - self.character_width - 5) + 60
            return GameState.PLAYING, (self.screen_width - self.character_width - 5, self.character_rect.y), self.ghost, self.item
        return None

    def update(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            new_rect = self.character_rect.move(-self.character_speed, 0)
            if 200 < new_rect.y < 405:
                self.character_rect.x -= self.character_speed
                self.current_image = self.character_left[self.left_index]
                self.frame_count += 1
                if self.frame_count % 10 == 0:
                    self.left_index = (self.left_index + 1) % 2

        elif keys[pygame.K_RIGHT]:
            new_rect = self.character_rect.move(self.character_speed, 0)
            if 200 < new_rect.y < 405 and self.character_rect.right < self.screen_width:
                self.character_rect.x += self.character_speed
                self.current_image = self.character_right[self.right_index]
                self.frame_count += 1
                if self.frame_count % 10 == 0:
                    self.right_index = (self.right_index + 1) % 2

        elif keys[pygame.K_UP]:
            new_rect = self.character_rect.move(0, -self.character_speed)
            if 200 < new_rect.y < 405:
                self.character_rect.y -= self.character_speed
                self.current_image = self.character_up

        elif keys[pygame.K_DOWN]:
            new_rect = self.character_rect.move(0, self.character_speed)
            if 200 < new_rect.y < 405:
                self.character_rect.y += self.character_speed
                self.current_image = self.character_down

        ghost_exit_zone = pygame.Rect(907, 329, 92, 68)

        if self.character_rect.colliderect(ghost_exit_zone):
            self.ghost = None

        if self.ghost:
            self.ghost.player = self.character_rect
            self.ghost.update()

        self.hedgehog1.update()
        self.hedgehog2.update()
        self.hedgehog3.update()

        if (self.hedgehog1.check_collision_with_character(self.character_rect)
                or self.hedgehog2.check_collision_with_character(self.character_rect)
                or self.hedgehog3.check_collision_with_character(self.character_rect)):
            self.item.picked_count -= 2

        if self.start_ticks:
            elapsed_time = pygame.time.get_ticks() - self.start_ticks
            self.remaining_time = (2 * 60 * 1000) - elapsed_time

    def draw(self, remaining_time):
        self.screen.blit(self.background_image, (0, 0))
        self.screen.blit(self.current_image, (self.character_rect.x, self.character_rect.y))
        if self.ghost:
            self.ghost.draw(self.screen)

        self.hedgehog1.draw(self.screen)
        self.hedgehog2.draw(self.screen)
        self.hedgehog3.draw(self.screen)

        minutes = remaining_time // 60000
        seconds = (remaining_time // 1000) % 60
        time_text = f"남은 시간: {minutes:02}:{seconds:02}"
        time_surface = self.font.render(time_text, True, (255, 255, 255))
        self.screen.blit(time_surface, (10, 15))
        self.screen.blit(self.item_image, (230, 15))

        picked_count_text = f"{self.item.picked_count}/10"
        picked_count_surface = self.font.render(picked_count_text, True, (255, 255, 255))
        self.screen.blit(picked_count_surface, (266, 15))

