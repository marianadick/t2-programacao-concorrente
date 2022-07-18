import globals
from threading import Thread
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

        # Pega o dicionário global de recursos e utiliza o nome da base como key
        # O value da key é uma lista [bool, bool] 
        # sendo o primeiro referente ao uranio e o segundo ao combustivel
        base_has_resources = globals.get_bases_has_resources()
        base_has_resources = base_has_resources[self.name]
        if (self.fuel < 120):
            base_has_resources[1] = False
        if (self.uranium < 35):
            base_has_resources[0]  = False


    def refuel_oil(self):
        mines = globals.get_mines_ref()
        oil_mine = mines['oil_earth']
        # Só uma base pode acessar a mina por vez
        globals.acquire_oil_mine()
        # A base sempre pegará o máximo possível de recursos
        # Sendo o limite a quantidade de recursos disponível ou a constraints
        if (oil_mine.unities <= self.constraints[1]):
            self.fuel += oil_mine.unities
            oil_mine.unities -= oil_mine.unities
        else:
            oil_mine.unities -= (self.constraints[1] - self.fuel)
            self.fuel += (self.constraints[1] - self.fuel)
        globals.release_oil_mine()
        if (self.fuel >= 120):
            # Pega o dicionário global de recursos e utiliza o nome da base como key
            # O value da key é uma lista [bool, bool] 
            # sendo o primeiro referente a uranio e o segundo a combustivel
            base_resources = globals.get_bases_has_resources()
            base_has_resources = base_resources[self.name]
            # Caso tenha recursos, define a variável como true
            base_has_resources[1] = True


    def refuel_uranium(self):
        mines = globals.get_mines_ref()
        uranium_mine = mines['uranium_earth']
        # Só uma base pode acessar a mina por vez
        globals.acquire_uranium_mine()
        # A base sempre pegará o máximo possível de recursos
        # Sendo o limite a quantidade de recursos disponível ou a constraints
        if (uranium_mine.unities <= self.constraints[0]):
            self.uranium += uranium_mine.unities
            uranium_mine.unities -= uranium_mine.unities
        else:
            uranium_mine.unities -= (self.constraints[0] - self.uranium)
            self.uranium += (self.constraints[0] - self.uranium)
        globals.release_uranium_mine() 
        if (self.uranium >= 35):
            # Pega o dicionário global de recursos e utiliza o nome da base como key
            # O value da key é uma lista [bool, bool] 
            # sendo o primeiro referente a uranio e o segundo a combustivel
            base_resources = globals.get_bases_has_resources()
            base_has_resources = base_resources[self.name]
            # Caso tenha recursos, define a variável como true
            base_has_resources[0] = True


    def supply_lion(self, rocket, moon):
        # Pega o minímo de recursos entre as restrições da mina e a capacidade do Lion
        oil_needed = min((moon.constraints[1] - moon.fuel), 120)
        uranium_needed = min((moon.constraints[0] - moon.uranium), 75)
        # Como a função refuel pega o quanto há disponível,
        # ele irá chamar ela até ter o necessário
        while (self.fuel < oil_needed):
            self.refuel_oil()
        while (self.uranium < uranium_needed):
            self.refuel_uranium()
        # Move os recursos para o Lion, removendo da base
        rocket.fuel_cargo += oil_needed
        rocket.uranium_cargo += uranium_needed
        self.fuel -= oil_needed
        self.uranium -= uranium_needed


    def get_random_planet(self):
        # Pega o dicionário global de planetas
        # Apenas os planetas não-terraformados permanecem no dict
        planets = globals.get_planets_ref()
        # Caso não tenham planetas, nada acontece
        if (len(planets) >= 1):
            # Seleciona planeta aleatório do dict para realizar o lançamento
            planet = random.choice(list(planets.values()))
            return planet


    def get_random_rocket(self):
        # Seleciona um tipo de foguete de maneira aleatória
        rockets = ['FALCON', 'DRAGON']
        index = random.randint(0,1)
        rocket_name = rockets[index]
        # Caso a base não seja a Lua, ela poderá lançar o Lion
        if (self.name != 'MOON'):
            # Apenas 1 base pode produzir o Lion
            globals.acquire_lion_production()
            # Verifica se há necessidade do Lion e se ele não foi lançado
            if (globals.get_lion_needed() and (not globals.get_lion_launched())):
                rocket_name = 'LION'
                # Informa que o Lion foi lançado
                globals.set_lion_launched(True)
            globals.release_lion_production()
        rocket = Rocket(rocket_name)
        self.rockets += 1
        return rocket


    def rocket_launch(self):
        # A base pode realizar apenas um lançamento por vez
        # Pega o dicionário global de locks, usa o nome como key, retorna uma lock
        base_launch_lock = globals.get_bases_locks()
        base_launch_lock = base_launch_lock[self.name][0]
        with base_launch_lock:
            # Pega um planeta e um rocket de forma aleatória
            planet = self.get_random_planet()
            rocket = self.get_random_rocket()
            # Decrementa os recursos da base necessários para o lançamento
            self.base_rocket_resources(rocket.name)
            # Caso seja o Lion, define o alvo como a Lua e carrega ele
            if (rocket.name == 'LION'):
                bases = globals.get_bases_ref()
                planet = bases['moon']
                self.supply_lion(rocket, planet)
            # Uma thread é utilizada para realizar o lançamento
            launcher = Launcher(self, rocket, planet)
            launcher.start()
            self.rockets -= 1


    def run(self):
        globals.acquire_print()
        self.print_space_base_info()
        globals.release_print()

        while(globals.get_release_system() == False):
            pass
        
        # Enquanto os 4 planetas não forem terraformados, a base opera
        while(not globals.get_end_project()):
            base_resources = globals.get_bases_has_resources()
            base_resources = base_resources[self.name]
            # Verifica se tem óleo e uranio
            base_has_oil = base_resources[1]
            base_has_uranium = base_resources[0]
            # Caso houver, lança um foguete
            if (base_has_oil and base_has_uranium):
                self.rocket_launch()
            # Caso contrário, se forem as bases da Terra
            # utiliza as minas para reabastecimento.
            # Se for a Lua, chama o Lion
            else:
                if (self.name != 'MOON'):
                    if (not base_has_uranium):
                        self.refuel_uranium()
                    if (not base_has_oil):
                        self.refuel_oil()
                else:
                    globals.set_lion_needed(True)
            # Checa se o projeto terminou
            globals.check_end_project()
