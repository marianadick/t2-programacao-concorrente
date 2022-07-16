import globals
from threading import Thread
from random import random
from space.bases import SpaceBase

from space.rocket import Rocket

class RocketLauncher(Thread):
    def __init__(self, rocket: Rocket, base: SpaceBase):
        Thread.__init__(self)
        self.rocket = rocket
        self.base = base
        
    def get_random_planet(self):
        planets = globals.get_planets_ref()
        planet = random.choice(list(planets.values()))
        return planet
        
    def run(self):
        planet = self.get_random_planet()
        self.rocket.launch(self.base, planet)