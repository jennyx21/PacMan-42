import time 


class Game():
    def __init__(self):
        self.start = False
        self.pause = False

    def game_info(self):
        return self.start, self.pause

    def update_start(self):
        if self.start is False:
            self.start = True
        elif self.start is True and self.pause is False:
            self.pause = True
        elif self.start is True and self.pause is True:
            self.pause = False
        time.sleep(0.2)
        return self.start


    # def update_direction:
