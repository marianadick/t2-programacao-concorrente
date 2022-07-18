import random
from time import sleep
import globals

class Rocket:

    ################################################
    # O CONSTRUTOR DA CLASSE NÃO PODE SER ALTERADO #
    ################################################
    def __init__(self, type):
        self.id = random.randrange(1000)
        self.name = type
        if(self.name == 'LION'):
            self.fuel_cargo = 0
            self.uranium_cargo = 0
            

    def nuke(self, planet): # Permitida a alteração
        
        damage = self.damage()
        
        # Pega os semáforos necessários para realizar o bombardeio
        planets_terraform_locks = globals.get_planets_terraform_locks()
        terraform_lock = planets_terraform_locks[planet.name][0]
        planets_pole_locks = globals.get_planets_pole_locks()
        south_pole_lock = planets_pole_locks[planet.name][1]
        north_pole_lock = planets_pole_locks[planet.name][0]
  
        # "Sorteia" o polo a ser foguetado
        # 0: Norte 1: Sul
        pole_draw = random.randint(0, 1)

        # Bombardeio ao Polo Norte
        if pole_draw == 0:
            # Lock para que apenas uma bomba chegue ao polo por vez
            north_pole_lock.acquire()
            print(f"[EXPLOSION] - The {self.name} ROCKET reached the planet {planet.name} on North Pole")
            terraform_lock.acquire()
            planet.terraform -= damage
            terraform_lock.release()
            north_pole_lock.release()
            
        # Bombardeio ao Polo Sul
        else:
            # Lock para que apenas uma bomba chegue ao polo por vez
            south_pole_lock.acquire()
            print(f"[EXPLOSION] - The {self.name} ROCKET reached the planet {planet.name} on South Pole")
            terraform_lock.acquire()
            planet.terraform -= damage
            terraform_lock.release()
            south_pole_lock.release()


    def voyage(self, planet):
        if (not globals.get_end_project()):
            # O tempo de viagem do Lion é desconsiderado
            if (self.name != 'LION'):
                self.simulation_time_voyage(planet)
            failure =  self.do_we_have_a_problem()
            # Caso especial de voyage para o Lion
            if (self.name == 'LION'):
                # Se falhar, define a variável de lançamento do Lion como false novamente
                if (failure):
                    globals.set_lion_launched(False)
                else:
                    # visto que é o lion sei que o 'planet' em questão é a lua
                    moon_has_resources = globals.get_bases_has_resources()
                    moon_has_resources = moon_has_resources['MOON']
                    # Passa os recursos do Lion para a Lua
                    planet.fuel += self.fuel_cargo
                    planet.uranium += self.uranium_cargo
                    # Caso haja os recursos necessários, retoma a produção
                    if (planet.uranium >= 35):
                        moon_has_resources[1] = True
                    if (planet.fuel >= 90):
                        moon_has_resources[0] = True
                    globals.set_lion_launched(False)
                    globals.set_lion_needed(False)
            # Se não for o Lion, nuka o planeta
            elif (not failure):
                # Verifica para ter certeza que não vamos matar ninguém
                if (planet.terraform > 0):
                    self.nuke(planet)



    ####################################################
    #                   ATENÇÃO                        # 
    #     AS FUNÇÕES ABAIXO NÃO PODEM SER ALTERADAS    #
    ###################################################
    def simulation_time_voyage(self, planet):
        if planet.name == 'MARS':
            sleep(2) # Marte tem uma distância aproximada de dois anos do planeta Terra.
        else:
            sleep(5) # IO, Europa e Ganimedes tem uma distância aproximada de cinco anos do planeta Terra.

    def do_we_have_a_problem(self):
        if(random.random() < 0.15):
            if(random.random() < 0.51):
                self.general_failure()
                return True
            else:
                self.meteor_collision()
                return True
        return False
            
    def general_failure(self):
        print(f"[GENERAL FAILURE] - {self.name} ROCKET id: {self.id}")
    
    def meteor_collision(self):
        print(f"[METEOR COLLISION] - {self.name} ROCKET id: {self.id}")

    def successfull_launch(self, base):
        if random.random() <= 0.1:
            if (self.name == 'LION'):
                globals.set_lion_launched(False)
            print(f"[LAUNCH FAILED] - {self.name} ROCKET id:{self.id} on {base.name}")
            return False
        return True
    
    def damage(self):
        return random.random()

    def launch(self, base, planet):
        if(self.successfull_launch(base)):
            print(f"[{self.name} - {self.id}] launched from {base.name}.")
            self.voyage(planet)        
