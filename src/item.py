import pygame

class Item:
    def __init__(self, item_image_path_before, item_image_path_after_full, item_image_path_after):
        self.item_image_before = pygame.image.load(item_image_path_before)
        self.item_image_after_full = pygame.image.load(item_image_path_after_full)
        self.item_image_after = pygame.image.load(item_image_path_after)
        self.current_item_image = None

        self.seed_planted = False
        self.watering_count = 0
        self.is_picked = False
        self.pick_time = None
        self.item_exists = False

        self.item_position = None

    def plant_seed(self, position):
        self.item_position = position
        self.current_item_image = self.item_image_before
        self.seed_planted = True
        self.item_exists = True
        self.watering_count = 0

    def water_seed(self):
        if self.seed_planted and self.watering_count < 5:
            self.watering_count += 1
            if self.watering_count == 5:
                self.current_item_image = self.item_image_after_full

    def draw_item(self, screen):
        if self.item_exists and self.item_position:
            screen.blit(self.current_item_image, self.item_position)

    def check_collision_move(self, character_rect):
        if self.item_position:
            item_rect = pygame.Rect(self.item_position[0], self.item_position[1], 32, 32)
            return item_rect.colliderect(character_rect)
        return False

    def check_collision_item(self, character_rect):
        item_rect = pygame.Rect(self.item_position[0], self.item_position[1], 32, 32)
        bottom_collision = (item_rect.top - 5 <= character_rect.bottom <= item_rect.top + 5)
        horizontal_collision = (item_rect.left - 20 <= character_rect.left <= item_rect.right - 20)
        return bottom_collision and horizontal_collision

    def check_if_grown(self):
        return self.seed_planted and self.watering_count >= 5

    def pick_item(self, current_time):
        if not self.is_picked:
            self.is_picked = True
            self.pick_time = current_time
            self.current_item_image = self.item_image_after
            self.item_exists = False
            return True
        return False

    def reset_item(self):
        self.is_picked = False
        self.pick_time = None
        self.item_exists = False
        self.item_position = False
        self.watering_count = 0
        self.seed_planted = False
        self.current_item_image = None