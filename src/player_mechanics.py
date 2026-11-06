import time


class Game():
    def __init__(self):
        self.start = False
        self.pause = False
        self.highscore = 0
        self.signal = 0

    def add_points(self, points: int):
        self.highscore += points

    def game_info(self) -> tuple[bool, bool]:
        return self.start, self.pause

    def update_start(self) -> None:
        if self.start is False:
            self.start = True
        elif self.start is True and self.pause is False:
            self.pause = True
        elif self.start is True and self.pause is True:
            self.pause = False
        time.sleep(0.2)

    def give_signal(self):
        self.signal = 1

    def reset_signal(self):
        self.signal = 0

    def update_edibility(self, edible_state: bool):
        if edible_state is False:
            return True
        else:
            return False
