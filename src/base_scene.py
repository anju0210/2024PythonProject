class BaseScene:
    def __init__(self, screen, character_pos=None, ghost=None, item=None):
        self.screen = screen
        self.screen_width, self.screen_height = 1080, 720
        self.initial_character_pos = character_pos
        self.initial_ghost = ghost
        self.initial_item = item

    def handle_event(self, event):
        return self.get_state(), None, None, None

    def update(self):
        pass

    def draw(self):
        pass

    def get_state(self):
        return None