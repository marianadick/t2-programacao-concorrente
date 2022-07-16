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
        # Talvez isso tenha que mudar de lugar! Discutir com Felipe
        self.terraform_lock = Lock()
        self.north_pole_hit_lock = Lock()
        self.south_pole_hit_lock = Lock()
        

    def nuke_detected(self, damage):
        ''' Não entendi o conceito dessa função então vou deixar comentado:
        while(self.terraform > 0):
            before_percentage = self.terraform
            while(before_percentage == self.terraform):
                pass
        '''
        while (self.terraform > 0):
            self.terraform_lock.acquire()
            self.terraform -= damage
            print(f"[NUKE DETECTION] - The planet {self.name} was bombed. {self.terraform}% UNHABITABLE")
            self.terraform_lock.release()
        # TO-DO: O que fazer quando habitável

    def print_planet_info(self):
        print(f"🪐 - [{self.name}] → {self.terraform}% UNINHABITABLE")

    def run(self):
        globals.acquire_print()
        self.print_planet_info()
        globals.release_print()

        while(globals.get_release_system() == False):
            pass

        while(True):
            self.nuke_detected()