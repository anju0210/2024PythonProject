import pygame
import sys
from game_state import GameState
from start import Start
from tutorial import Tutorial
from game import Game
from next_scene import NextScene
from ending import HappyEnding, SadEnding


class Main:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1080, 720))
        pygame.display.set_caption("Farm Game")
        self.clock = pygame.time.Clock()
        self.initialize_game()

    def initialize_game(self):
        self.current_state = GameState.START
        self.character_pos = None
        self.ghost = None
        self.item = None
        self.start_ticks = None
        self.remaining_time = 60 * 2000

        self.scenes = {
            GameState.START: Start(self.screen),
            GameState.TUTORIAL: Tutorial(self.screen),
            GameState.PLAYING: Game(self.screen),
            GameState.PLAYING_NEXT: NextScene(self.screen),
            GameState.HAPPYENDING: HappyEnding(self.screen),
            GameState.SADENDING: SadEnding(self.screen)
        }

    def run(self):
        running = True
        while running:

            current_scene = self.scenes[self.current_state]

            if self.start_ticks is None and self.current_state == GameState.PLAYING:
                self.start_ticks = pygame.time.get_ticks()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                new_state, new_char_pos, new_ghost, new_item = current_scene.handle_event(event)
                if new_state != self.current_state:
                    self.character_pos = new_char_pos
                    self.ghost = new_ghost
                    self.item = new_item
                    self.current_state = new_state

                    if self.current_state == GameState.START:
                        self.initialize_game()
                    else:
                        self.scenes[self.current_state] = self.scenes[self.current_state].__class__(
                            self.screen, self.character_pos, self.ghost, self.item, self.start_ticks, self.remaining_time
                        )

            if self.start_ticks:
                elapsed_time = pygame.time.get_ticks() - self.start_ticks
                self.remaining_time = (60 * 2000) - elapsed_time

            if self.remaining_time <= 0 and (self.current_state == GameState.PLAYING or self.current_state == GameState.PLAYING_NEXT) :
                picked_count = self.item.picked_count if self.item else 0
                if picked_count >= 10:
                    self.current_state = GameState.HAPPYENDING
                else:
                    self.current_state = GameState.SADENDING

            current_scene.update()
            current_scene.draw(self.remaining_time)
            pygame.display.flip()
            self.clock.tick(60)


        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = Main()
    game.run()


