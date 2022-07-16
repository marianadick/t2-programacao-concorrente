from resource import prlimit
import globals
from threading import Thread, Lock
from space.rocket import Rocket
import random
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
        #nao pode mexer pipipopopo
        self.base_launch_lock = Lock()
        self.base_has_oil = False
        self.base_has_uranium = False

    def print_space_base_info(self):
        print(f"🔭 - [{self.name}] → 🪨  {self.uranium}/{self.constraints[0]} URANIUM  ⛽ {self.fuel}/{self.constraints[1]}  🚀 {self.rockets}/{self.constraints[2]}")


    def base_rocket_resources(self, rocket_name):

        match rocket_name:
            case 'DRAGON':
                self.uranium = self.uranium - 35
                if self.name == 'ALCANTARA':
                    self.fuel = self.fuel - 70
                elif self.name == 'MOON':
                    self.fuel = self.fuel - 50
                else:
                    self.fuel = self.fuel - 100
            case 'FALCON':
                self.uranium = self.uranium - 35
                if self.name == 'ALCANTARA':
                    self.fuel = self.fuel - 100
                elif self.name == 'MOON':
                    self.fuel = self.fuel - 90
                else:
                    self.fuel = self.fuel - 120
            case 'LION':
                if self.name == 'ALCANTARA':
                    self.fuel = self.fuel - 100
                else:
                    self.fuel = self.fuel - 115
            case _:
                print("Invalid rocket name")

        if (self.fuel < 120):
            self.base_has_oil = False
        if (self.uranium < 35):
            self.base_has_uranium = False

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
        if (self.fuel >= 120):
            self.base_has_oil = True

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
        if (self.uranium >= 35):
            self.base_has_uranium = True

    def supply_lion(self, rocket, moon):
        oil_needed = min((moon.constraints[1] - moon.fuel), 120)
        uranium_needed = min((moon.constraints[0] - moon.uranium), 75)
        while (self.fuel < oil_needed):
            self.refuel_oil()
        while (self.uranium < uranium_needed):
            self.refuel_uranium()
        rocket.fuel_cargo += oil_needed
        rocket.uranium_cargo += uranium_needed
        self.fuel -= oil_needed
        self.uranium -= uranium_needed

    def get_random_planet(self):
        planets = globals.get_planets_ref()
        planet = random.choice(list(planets.values()))
        return planet

    def get_random_rocket(self):
        rockets = ['FALCON', 'DRAGON']
        index = random.randint(0,1)
        rocket_name = rockets[index]
        if (self.name != 'MOON'):
            globals.acquire_lion_production()
            if (globals.get_lion_needed() and (not globals.get_lion_launched())):
                rocket_name = 'LION'
                globals.set_lion_launched(True)
            globals.release_lion_production()
        rocket = Rocket(rocket_name)
        self.rockets += 1
        return rocket
        
    def rocket_launch(self):
        with self.base_launch_lock:
            planet = self.get_random_planet()
            rocket = self.get_random_rocket()
            self.base_rocket_resources(rocket.name)
            if (rocket.name == 'LION'):
                bases = globals.get_bases_ref()
                planet = bases['moon']
                self.supply_lion(rocket, planet)
            launcher = Launcher(self, rocket, planet)
            launcher.start()
            self.rockets -= 1

    def run(self):
        globals.acquire_print()
        self.print_space_base_info()
        globals.release_print()

        while(globals.get_release_system() == False):
            pass

        while(True):
            if (self.base_has_oil and self.base_has_uranium):
                self.rocket_launch()
            else:
                if (self.name != 'MOON'):
                    if (not self.base_has_uranium):
                        self.refuel_uranium()
                    if (not self.base_has_oil):
                        self.refuel_oil()
                else:
                    globals.set_lion_needed(True)
