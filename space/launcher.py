from threading import Thread

from space.bases import SpaceBase
from space.rocket import Rocket
from stars.planet import Planet

class Launcher(Thread):
    def __init__(self, base: SpaceBase, rocket: Rocket, planet: Planet):
        Thread.__init__(self)
        self.base = base
        self.rocket = rocket
        self.planet = planet

        
    def run(self):
        self.rocket.launch(self.base, self.planet)