import pygame
from game_state import GameState
from base_scene import BaseScene
from item import Item
from ghost import Ghost


class Game(BaseScene):
    def __init__(self, screen, character_pos=None, ghost=None, item=None, start_ticks=None, remaining_time=None):
        super().__init__(screen, character_pos, ghost, item)
        self.start_ticks = start_ticks
        self.remaining_time = remaining_time
        self.font = pygame.font.Font("DungGeunMo.ttf", 24)

        self.character_width, self.character_height = 44, 80
        if character_pos:
            self.character_x, self.character_y = character_pos
        else:
            self.character_x = self.screen_width // 2 - self.character_width // 2
            self.character_y = self.screen_height // 2 - self.character_height // 2
        self.character_speed = 5

        self.character_rect = pygame.Rect(self.character_x, self.character_y, self.character_width, self.character_height)

        self.background_image = pygame.image.load("../assets/images/game_background.png").convert()
        self.background_image = pygame.transform.scale(self.background_image, (1080, 720))

        self.character_up = pygame.image.load("../assets/images/ham_up.png").convert_alpha()
        self.character_down = pygame.image.load("../assets/images/ham_down.png").convert_alpha()
        self.character_left = [
            pygame.image.load("../assets/images/ham_left1.png").convert_alpha(),
            pygame.image.load("../assets/images/ham_left2.png").convert_alpha()
        ]
        self.character_right = [
            pygame.image.load("../assets/images/ham_right1.png").convert_alpha(),
            pygame.image.load("../assets/images/ham_right2.png").convert_alpha()
        ]
        self.character_pick = pygame.image.load("../assets/images/ham_pick.png").convert_alpha()
        self.water_droplet_image = pygame.image.load("../assets/images/water_droplet.png").convert_alpha()
        self.item_image = pygame.image.load("../assets/images/item_after.png").convert_alpha()
        self.item_image = pygame.transform.scale(self.item_image, (28, 28))

        if item:
            self.item = item
        else:
            self.item = Item("../assets/images/item_before.png",
                         "../assets/images/item_after_full.png",
                         "../assets/images/item_after.png",
                             "../assets/images/item_die.png")

        if ghost:
            self.ghost = ghost
            self.ghost.player = None
        else:
            self.ghost = Ghost(self.screen_width, self.screen_height, None)

        self.current_image = self.character_down
        self.left_index = 0
        self.right_index = 0
        self.frame_count = 0

        self.water_droplet_time = None
        self.water_droplet_duration = 300
        self.water_droplet_position = None

    def handle_event(self, event):
        current_time = pygame.time.get_ticks()

        screen_transition = self.check_screen_transition(self.character_rect)
        if screen_transition:
            return screen_transition

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not self.ghost.is_visible:
                self.item.plant_seed((self.character_rect.x,
                                      (self.character_rect.y + self.character_height)))

            if event.key == pygame.K_RETURN:
                seed = self.item.check_collision_item(self.character_rect)
                if seed and seed['watering_count']>=5 and not self.ghost.is_visible:
                    self.item.die_item(seed, current_time)
                    self.water_droplet_time = current_time
                    self.water_droplet_position = (seed['position'][0] - 10,
                                                   seed['position'][1] - 60)
                elif seed and not self.ghost.is_visible:
                    if self.item.water_seed(seed):
                        self.water_droplet_time = current_time
                        self.water_droplet_position = (seed['position'][0] - 10,
                                                       seed['position'][1] - 60)

            if event.key == pygame.K_e:
                self.current_image = self.character_pick
                seed = self.item.check_collision_item(self.character_rect)
                if seed and seed['watering_count'] >= 5 and not self.ghost.is_visible:
                    self.item.pick_item(seed, current_time)
                elif seed and seed['watering_count'] < 5 and not self.ghost.is_visible:
                    self.item.die_item(seed, current_time)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_e:
                self.current_image = self.character_down

        return GameState.PLAYING, None, None, self.item

    def check_screen_transition(self, character_rect):
        if self.character_rect.x >= self.screen_width - self.character_width and 200 < self.character_rect.y < 405:
            if self.ghost:
                self.ghost.rect.x = -60
            return GameState.PLAYING_NEXT, (0, self.character_rect.y), self.ghost, self.item
        return None

    def update(self):
        current_time = pygame.time.get_ticks()
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            new_rect = self.character_rect.move(-self.character_speed, 0)
            if not self.item.check_collision_move(new_rect) and self.character_rect.left > 0:
                self.character_rect.x -= self.character_speed
                self.current_image = self.character_left[self.left_index]
                self.frame_count += 1
                if self.frame_count % 10 == 0:
                    self.left_index = (self.left_index + 1) % 2

        elif keys[pygame.K_RIGHT]:
            new_rect = self.character_rect.move(self.character_speed, 0)
            if not self.item.check_collision_move(
                    new_rect) and self.character_rect.right < self.screen_width:
                self.character_rect.x += self.character_speed
                self.current_image = self.character_right[self.right_index]
                self.frame_count += 1
                if self.frame_count % 10 == 0:
                    self.right_index = (self.right_index + 1) % 2

        elif keys[pygame.K_UP]:
            new_rect = self.character_rect.move(0, -self.character_speed)
            if not self.item.check_collision_move(new_rect) and self.character_rect.top > 0:
                self.character_rect.y -= self.character_speed
                self.current_image = self.character_up

        elif keys[pygame.K_DOWN]:
            new_rect = self.character_rect.move(0, self.character_speed)
            if not self.item.check_collision_move(
                    new_rect) and self.character_rect.bottom < self.screen_height:
                self.character_rect.y += self.character_speed
                self.current_image = self.character_down

        for seed in self.item.seeds:
            if seed['is_picked'] and current_time - seed['pick_time'] >= 1000:
                self.item.reset_items(seed)

        if self.ghost:
            self.ghost.player = self.character_rect
            self.ghost.update()


        if self.start_ticks:
            elapsed_time = pygame.time.get_ticks() - self.start_ticks
            self.remaining_time = (2 * 60 * 1000) - elapsed_time


    def draw(self, remaining_time):
        current_time = pygame.time.get_ticks()

        self.screen.blit(self.background_image, (0, 0))
        self.item.draw_items(self.screen)
        self.screen.blit(self.current_image, (self.character_rect.x, self.character_rect.y))

        if (self.water_droplet_time and
                current_time - self.water_droplet_time < self.water_droplet_duration):
            self.screen.blit(self.water_droplet_image, self.water_droplet_position)
        else:
            self.water_droplet_time = None

        if self.ghost:
            self.ghost.draw(self.screen)

        minutes = remaining_time // 60000
        seconds = (remaining_time // 1000) % 60
        time_text = f"남은 시간: {minutes:02}:{seconds:02}"
        time_surface = self.font.render(time_text, True, (255, 255, 255))
        self.screen.blit(time_surface, (10, 15))
        self.screen.blit(self.item_image, (230, 15))

        picked_count_text = f"{self.item.picked_count}/10"
        picked_count_surface = self.font.render(picked_count_text, True, (255, 255, 255))
        self.screen.blit(picked_count_surface, (266, 15))

