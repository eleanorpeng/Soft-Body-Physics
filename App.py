import pygame as game

class App:
    running = True
    screen = None
    title = "Application"
    size = (0, 0)
    center = (0, 0)
    flags = game.HWSURFACE | game.DOUBLEBUF
    frame_rate = 30

    def __init__(self, t="Application", x=550, y=400, f=30):
        self.title = t
        self.size = (x, y)
        self.center = (x/2, y/2)
        self.frame_rate = f
        self.initialize()

    def run(self):
        game.init()
        game.display.set_caption(self.title)
        self.screen = game.display.set_mode(self.size, self.flags)
        self.running = True

        while self.running:
            for event in game.event.get():
                self.handle_event(event)
            self.update()
            self.render()
            game.time.delay(int(1000 / self.frame_rate))
        self.clean_up()

    def handle_event(self, event):
        if event.type == game.QUIT:
            self.running = False

    def clean_up(self):
        game.quit()

    def exit(self):
        self.running = False

    def initialize(self):
        pass

    def update(self):
        pass

    def render(self):
        pass