import pygame

class Item:
    def __init__(self, item_image_path_before, item_image_path_after_full, item_image_path_after, item_image_path_die):
        self.item_image_before = pygame.image.load(item_image_path_before).convert_alpha()
        self.item_image_before = pygame.transform.scale(self.item_image_before, (32, 32))
        self.item_image_after_full = pygame.image.load(item_image_path_after_full).convert_alpha()
        self.item_image_after_full = pygame.transform.scale(self.item_image_after_full, (32, 32))
        self.item_image_after = pygame.image.load(item_image_path_after).convert_alpha()
        self.item_image_die = pygame.image.load(item_image_path_die).convert_alpha()
        self.item_image_die = pygame.transform.scale(self.item_image_die, (32, 32))

        self.can_move = False
        self.seeds = []
        self.max_seeds = 10
        self.picked_count = 0


    def plant_seed(self, position):
        new_item_rect = pygame.Rect(position[0], position[1], 32, 32)

        for seed in self.seeds:
            existing_seed_rect = pygame.Rect(seed["position"][0], seed["position"][1], 32, 32)
            if new_item_rect.colliderect(existing_seed_rect):
                return

        if len(self.seeds) < self.max_seeds:
            print(len(self.seeds))
            self.seeds.append({
                'position': position,
                'current_image': self.item_image_before,
                'watering_count': 0,
                'is_picked': False,
                'pick_time': 0,
                'is_grown': False,
                'last_watered_time': 0
            })

    def water_seed(self, seed):
        current_time = pygame.time.get_ticks()

        if current_time - seed.get('last_watered_time', 0) < 2000:
            return False

        if seed["watering_count"] < 5:
            seed["watering_count"] += 1
            seed['last_watered_time'] = current_time
            if seed["watering_count"] > 2:
                seed["current_image"] = self.item_image_after_full
                if seed["watering_count"] == 5:
                    seed["is_grown"] = True

        return True

    def draw_items(self, screen):
        current_time = pygame.time.get_ticks()
        for seed in self.seeds[:]:
            screen.blit(seed['current_image'], seed['position'])

            if seed['is_grown'] and seed['pick_time'] == 0:
                seed['pick_time'] = current_time

            if seed['is_grown'] and current_time - seed['pick_time'] > 10000 and not seed['is_picked']:
                self.reset_items(seed)

    def check_collision_item(self, character_rect):
        for seed in self.seeds:
            item_rect = pygame.Rect(seed['position'][0], seed['position'][1], 32, 32)
            bottom_collision = (item_rect.top - 5 <= character_rect.bottom <= item_rect.top + 5)
            horizontal_collision = (item_rect.left - 20 <= character_rect.left <= item_rect.right - 20)
            if bottom_collision and horizontal_collision and not seed['is_picked']:
                return seed
        return None

    def check_collision_move(self, character_rect):
        for seed in self.seeds:
            item_rect = pygame.Rect(seed['position'][0], seed['position'][1], 32, 1)
            if item_rect.colliderect(character_rect):
                return True
        return False

    def pick_item(self, seed, current_time):
        seed['is_picked'] = True
        seed['current_image'] = self.item_image_after
        seed['pick_time'] = current_time
        self.picked_count += 1

    def die_item(self, seed, current_time):
        seed['is_picked'] = True
        seed['current_image'] = self.item_image_die
        seed['pick_time'] = current_time

    def reset_items(self, seed):
        if seed in self.seeds:
            self.seeds.remove(seed)
