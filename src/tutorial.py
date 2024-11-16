import pygame
from game_state import GameState
from base_scene import BaseScene

class Tutorial(BaseScene):
    def __init__(self, screen, character_pos=None, ghost=None, item=None, start_ticks=None, remaining_time=None):
        super().__init__(screen, character_pos, ghost, item)

        self.background = pygame.image.load("../assets/images/tutorial_background.png").convert()

        self.font = pygame.font.Font("DungGeunMo.ttf", 24)
        self.texts = [
            [
                "나는 얼마 전 도시 생활에 지쳐 귀농을 한 쥐다!",
                "집들이 겸 친구들을 초대해서",
                "직접 키운 치즈로 맛있는 저녁 식사를 해주고 싶다",
                "그런데 오늘따라 내 텃밭이 어둡고 서늘한 것 같다",
                "그래도 친구들이 오는 시간에 맞춰",
                "저녁을 준비하려면 지체할 시간이 없다",
                "얼른 치즈를 키워서 캐오자!"
            ],
            [
                "조작법",
                "방향키: 이동하기",
                "Space: 씨앗 심기",
                "Enter: 물주기",
                "E: 수확하기",
            ],
            [
                "유령이 돌아다니는 동안은 아무것도 할 수 없다",
                "유령을 쫓아내려면 텃밭의 오른쪽으로 가라",
                "가는 길에 고슴도치에게 치즈를 빼앗기지 않도록 주의할 것!",
                "",
                "새싹에 물은 주는 것은 정확히 5번만!",
                "더 많이 주거나 적게 주면 새싹은 시들어버린다",
                "",
                "다 자라난 싹을 10초 안에 뽑지 못하면 두더지가 치즈를 훔쳐간다"
            ]
        ]
        self.current_step = 0

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if self.current_step < len(self.texts) - 1:
                    self.current_step += 1
                else:
                    return GameState.PLAYING, None, None, None
        return GameState.TUTORIAL, None, None, None

    def update(self):
        pass


    def draw(self, time):
        self.screen.blit(self.background, (0, 0))
        y_offset = 200
        line_spacing = 40
        for line in self.texts[self.current_step]:
            text_surface = self.font.render(line, True, (75, 41, 11))
            text_rect = text_surface.get_rect(center=(self.screen.get_width() // 2, y_offset))
            self.screen.blit(text_surface, text_rect)
            y_offset += line_spacing