from threading import Thread

class Launcher(Thread):
    def __init__(self, base, rocket, planet):
        Thread.__init__(self, daemon=True)
        self.base = base
        self.rocket = rocket
        self.planet = planet

    def run(self):
        self.rocket.launch(self.base, self.planet)
