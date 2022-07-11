import globals
from threading import Thread
from space.rocket import Rocket
from random import choice

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
                    print("FAlhou, sem recursos")
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
                    print("FAlhou, sem recursos")
            case 'LION':
                if self.uranium >= 35 and self.fuel >= 100:
                    self.uranium = self.uranium - 35
                    if self.name == 'ALCANTARA':
                        self.fuel = self.fuel - 100
                    else:
                        self.fuel = self.fuel - 115
                else:
                    print("FAlhou, sem recursos")
            case _:
                print("Invalid rocket name")


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
        

    def run(self):
        globals.acquire_print()
        self.print_space_base_info()
        globals.release_print()

        while(globals.get_release_system() == False):
            pass

        while(True):

            pass
