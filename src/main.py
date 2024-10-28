import pygame
import sys
from item import Item

pygame.init()

screen_width, screen_height = 1080, 720
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Character Movement with Items")

WHITE = (255, 255, 255)

character_width, character_height = 44, 80
character_x = screen_width // 2 - character_width // 2
character_y = screen_height // 2 - character_height // 2
character_speed = 5

# 캐릭터 이미지
character_up = pygame.image.load("../assets/images/ham_up.png")
character_down = pygame.image.load("../assets/images/ham_down.png")
character_left = [pygame.image.load("../assets/images/ham_left1.png"),
                  pygame.image.load("../assets/images/ham_left2.png")]
character_right = [pygame.image.load("../assets/images/ham_right1.png"),
                   pygame.image.load("../assets/images/ham_right2.png")]
character_pick = pygame.image.load("../assets/images/ham_pick.png")

water_droplet_image = pygame.image.load("../assets/images/water_droplet.png")  # 물방울 이미지

item = Item("../assets/images/item_before.png", "../assets/images/item_after_full.png", "../assets/images/item_after.png")

current_image = character_down

left_index = 0
right_index = 0
frame_count = 0
is_picking = False
pick_time = None
is_watering = False
water_time = None
water_droplet_time = None
water_droplet_duration = 500

running = True
while running:
    current_time = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()

    character_rect = pygame.Rect(character_x, character_y, character_width, character_height)

    if keys[pygame.K_LEFT]:
        new_rect = character_rect.move(-character_speed, 0)
        if not item.check_collision_move(new_rect):
            character_x -= character_speed
            current_image = character_left[left_index]
            frame_count += 1
            if frame_count % 10 == 0:
                left_index = (left_index + 1) % 2

    elif keys[pygame.K_RIGHT]:
        new_rect = character_rect.move(character_speed, 0)
        if not item.check_collision_move(new_rect):
            character_x += character_speed
            current_image = character_right[right_index]
            frame_count += 1
            if frame_count % 10 == 0:
                right_index = (right_index + 1) % 2

    elif keys[pygame.K_UP]:
        new_rect = character_rect.move(0, -character_speed)
        if not item.check_collision_move(new_rect):
            character_y -= character_speed
            current_image = character_up

    elif keys[pygame.K_DOWN]:
        new_rect = character_rect.move(0, character_speed)
        current_image = character_down
        if not item.check_collision_move(new_rect):
            character_y += character_speed

    # 씨앗 심기
    if keys[pygame.K_SPACE] and not item.seed_planted:
        item.plant_seed((character_x, (character_y + character_height)))

    # 물 주기
    if keys[pygame.K_RETURN] and not is_watering:
        if item.seed_planted and item.check_collision_item(character_rect):
            item.water_seed()
            is_watering = True
            water_droplet_time = current_time

    if item.check_if_grown():
        is_watering = False

    # 물방울
    if is_watering and current_time - water_droplet_time >= water_droplet_duration:
        is_watering = False
        water_droplet_time = None

    # 아이템 줍기
    if keys[pygame.K_SPACE] and item.check_if_grown():
        if item.check_collision_item(character_rect):
            item.item_exists = True
            item.pick_item(current_time)

    if item.is_picked and current_time - item.pick_time >= 1000:
        item.item_exists = False
        item.reset_item()

    screen.fill(WHITE)

    screen.blit(current_image, (character_x, character_y))  # 캐릭터 이미지

    item.draw_item(screen)

    # 물방울 이미지 그리기
    if is_watering:
        water_droplet_x = character_x + (character_width - 36) // 2
        water_droplet_y = item.item_position[1] - 62
        screen.blit(water_droplet_image, (water_droplet_x, water_droplet_y))

    pygame.display.flip()

    pygame.time.Clock().tick(60)