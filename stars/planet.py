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

            # Não há valores negativos de terraformação
            if self.terraform <= 0:
                self.terraform = 0
                name = self.name.lower()
                # caso a terraformação esteja completa, isso é definido no dict terraform_completed
                # essa variável é utilizada para finalizar o programa
                planets_end = globals.get_terraform_completed()
                planets_end[self.name][0] = True
                # removemos o planeta do dict de planetas
                # isso faz parte da lógica de escolha de foguetes do nosso programa
                planets = globals.get_planets_ref()
                del planets[name]

            print(f"[NUKE DETECTION] - The planet {self.name} was bombed. {self.terraform:.2f}% UNHABITABLE")


    def print_planet_info(self):
        planets_terraform_locks = globals.get_planets_terraform_locks()
        terraform_lock = planets_terraform_locks[self.name][0]
        # Apenas uma base pode acessar as infos do planeta por vez
        terraform_lock.acquire()
        print(f"🪐 - [{self.name}] → {self.terraform}% UNINHABITABLE")
        terraform_lock.release()


    def run(self):
        
        globals.acquire_print()
        self.print_planet_info()
        globals.release_print()

        while(globals.get_release_system() == False):
            pass

        self.nuke_detected()
