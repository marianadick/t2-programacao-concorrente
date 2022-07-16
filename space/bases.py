import globals
from threading import Thread
from space.rocket import Rocket
from random import random, choice

from space.launcher import Launcher

class SpaceBase(Thread):

    ################################################
    # O CONSTRUTOR DA CLASSE NÃO PODE SER ALTERADO #
    ################################################
    def __init__(self, name, fuel, uranium, rockets):
        Thread.__init__(self)
        self.name = name
        self.uranium = 0
        self.fuel = 0
        self.rockets = 0
        self.constraints = [uranium, fuel, rockets]

    def print_space_base_info(self):
        print(f"🔭 - [{self.name}] → 🪨  {self.uranium}/{self.constraints[0]} URANIUM  ⛽ {self.fuel}/{self.constraints[1]}  🚀 {self.rockets}/{self.constraints[2]}")


    def base_rocket_resources(self, rocket_name):

        base_has_resource = True
        
        if (self.name != 'MOON'):
            while (self.uranium < 35):
                self.refuel_uranium()
            while (self.fuel < 120):
                self.refuel_oil()
        else:
            self.requeset_lion()


        match rocket_name:
            case 'DRAGON':
                if self.uranium >= 35 and self.fuel >= 100:
                    self.uranium = self.uranium - 35
                    if self.name == 'ALCANTARA':
                        self.fuel = self.fuel - 70
                    elif self.name == 'MOON':
                        self.fuel = self.fuel - 50
                    else:
                        self.fuel = self.fuel - 100
                else:
                    print("Falhou, sem recursos")
                    base_has_resource = False
            case 'FALCON':
                if self.uranium >= 35 and self.fuel >= 120:
                    self.uranium = self.uranium - 35
                    if self.name == 'ALCANTARA':
                        self.fuel = self.fuel - 100
                    elif self.name == 'MOON':
                        self.fuel = self.fuel - 90
                    else:
                        self.fuel = self.fuel - 120
                else:
                    print("Falhou, sem recursos")
                    base_has_resource = False
            case 'LION':
                if self.uranium >= 35 and self.fuel >= 100:
                    self.uranium = self.uranium - 35
                    if self.name == 'ALCANTARA':
                        self.fuel = self.fuel - 100
                    else:
                        self.fuel = self.fuel - 115
                else:
                    print("Falhou, sem recursos")
                    base_has_resource = False
            case _:
                print("Invalid rocket name")

        return base_has_resource

    def refuel_oil(self):
        mines = globals.get_mines_ref()
        oil_mine = mines['oil_earth']
        globals.acquire_oil_mine()
        if (oil_mine.unities <= self.constraints[1]):
            self.fuel += oil_mine.unities
            oil_mine.unities -= oil_mine.unities
        else:
            oil_mine.unities -= (self.constraints[1] - self.fuel)
            self.fuel += (self.constraints[1] - self.fuel)
        globals.release_oil_mine()

    def refuel_uranium(self):
        mines = globals.get_mines_ref()
        uranium_mine = mines['uranium_earth']
        globals.acquire_uranium_mine()
        if (uranium_mine.unities <= self.constraints[0]):
            self.uranium += uranium_mine.unities
            uranium_mine.unities -= uranium_mine.unities
        else:
            uranium_mine.unities -= (self.constraints[0] - self.uranium)
            self.uranium += (self.constraints[0] - self.uranium)
        globals.release_uranium_mine() 


    def requeset_lion():
        bases = globals.get_bases_ref()
        
    def get_random_planet():
        planets = globals.get_planets_ref
        planet = random.choice(list(planets.values()))
        return planet

    def get_random_rocket():
        rocket_draw = random.randint(0, 1)
        rockets = ['DRAGON', 'FALCON']
        rocket = Rocket(rockets[rocket_draw])
        return rocket
        
    def rocket_launch(self):
        planet = self.get_random_planet
        rocket = self.get_random_rocket
        base_has_resource = self.base_rocket_resources(rocket.name)
        if base_has_resource:
            launcher = Launcher(self, rocket, planet)
            launcher.start()

    def run(self):
        globals.acquire_print()
        self.print_space_base_info()
        globals.release_print()

        while(globals.get_release_system() == False):
            pass

        while(True):

            self.rocket_launch()
