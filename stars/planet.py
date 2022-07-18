from threading import Thread, Semaphore, Lock
import globals

class Planet(Thread):

    ################################################
    # O CONSTRUTOR DA CLASSE NÃO PODE SER ALTERADO #
    ################################################
    def __init__(self, terraform, name):
        Thread.__init__(self)
        self.terraform = terraform
        self.name = name
        

    def nuke_detected(self):
        while(self.terraform > 0):
            before_percentage = self.terraform
            while(before_percentage == self.terraform):
                pass

            if self.terraform < 0:
                self.terraform = 0

            print(f"[NUKE DETECTION] - The planet {self.name} was bombed. {self.terraform}% UNHABITABLE")

        # TO-DO: O que fazer quando habitável

    def print_planet_info(self):
        planets_terraform_locks = globals.get_planets_terraform_locks()
        terraform_lock = planets_terraform_locks[self.name][0]
        terraform_lock.acquire()
        print(f"🪐 - [{self.name}] → {self.terraform}% UNINHABITABLE")
        terraform_lock.release()

    def run(self):
        
        globals.acquire_print()
        self.print_planet_info()
        globals.release_print()

        while(globals.get_release_system() == False):
            pass

        while(True):
            self.nuke_detected()
            name = self.name.lower()
            planets = globals.get_planets_ref()
            del planets[name]
            break
