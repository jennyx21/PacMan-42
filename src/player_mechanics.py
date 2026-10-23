class Game():
    def __init__(self):
        self.start = False

    def game_info(self):
        return self.start

    def update_start(self):
        self.start = True
        return self.start

    # def update_direction:
