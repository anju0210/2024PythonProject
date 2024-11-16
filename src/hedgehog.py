import pygame

class Hedgehog:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 32
        self.height = 32
        self.image = pygame.image.load("../assets/images/hedgehog.png")
        self.image = pygame.transform.scale(self.image, (68,48))
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.speed = 2
        self.direction = 1

        self.has_collided = False

    def update(self):
        if self.rect.top <= 200 or self.rect.bottom >= 420:
            self.direction *= -1

        self.rect.y += self.speed * self.direction

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)

    def check_collision_with_character(self, character_rect):
        if self.rect.colliderect(character_rect):
            if not self.has_collided:
                self.has_collided = True
                return True
        else:
            self.has_collided = False
        return False