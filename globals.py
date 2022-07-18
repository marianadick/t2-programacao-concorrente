from threading import Lock, Condition

#  A total alteração deste arquivo é permitida.
#  Lembre-se de que algumas variáveis globais são setadas no arquivo simulation.py
#  Portanto, ao alterá-las aqui, tenha cuidado de não modificá-las. 
#  Você pode criar variáveis globais no código fora deste arquivo, contudo, agrupá-las em
#  um arquivo como este é considerado uma boa prática de programação. Frameworks como o Redux,
#  muito utilizado em frontend em libraries como o React, utilizam a filosofia de um store
#  global de estados da aplicação e está presente em sistemas robustos pelo mundo.

release_system = False
mutex_print = Lock()
uranium_mine_acess = Lock()
oil_mine_acess = Lock()
lion_lock = Lock()
planets = {}
bases = {}
mines = {}
simulation_time = None
lion_needed = False
lion_launched = False

alcantara_lock = Lock()
canaveral_lock = Lock()
moscow_lock = Lock()
moon_lock = Lock()

mars_terraform_lock = Lock()
io_terraform_lock = Lock()
ganimedes_terraform_lock = Lock()
europa_terraform_lock = Lock()

mars_north_pole_lock = Lock()
io_north_pole_lock = Lock()
ganimedes_north_pole_lock = Lock()
europa_north_pole_lock = Lock()

mars_south_pole_lock = Lock()
io_south_pole_lock = Lock()
ganimedes_south_pole_lock = Lock()
europa_south_pole_lock = Lock()
satelite_lock = Lock()
end_project = False
count = 0
mines_stop = False

# Sincronização para finalizar as minas
def get_mines_stop():
    global mines_stop
    return mines_stop

# Locks das plataformas de lançamento das bases
bases_locks = {
    'ALCANTARA': [alcantara_lock],
    'CANAVERAL CAPE': [canaveral_lock],
    'MOSCOW': [moscow_lock],
    'MOON': [moon_lock]
}

# Booleanos de recursos das bases
# [False, False] = o primeiro referente a uranio e o segundo a combustivel
bases_has_resources = {
    'ALCANTARA': [False, False],
    'CANAVERAL CAPE': [False, False],
    'MOSCOW': [False, False],
    'MOON': [False, False]
}

# Locks de acesso as informações de terraformação dos planetas
planets_terraform_locks = {
    'MARS': [mars_terraform_lock],
    'IO': [io_terraform_lock],
    'GANIMEDES': [ganimedes_terraform_lock],
    'EUROPA': [europa_terraform_lock]
}

# Locks dos polos do planeta, impedem que mais de uma bomba exploda no mesmo polo
planets_pole_locks = {
    'MARS': [mars_north_pole_lock, mars_south_pole_lock],
    'IO': [io_north_pole_lock, io_south_pole_lock],
    'GANIMEDES': [ganimedes_north_pole_lock, ganimedes_south_pole_lock],
    'EUROPA': [europa_north_pole_lock, europa_south_pole_lock]
}

# Variáveis que informam se a terraformação está completa
terraform_completed = {
    'MARS': [False],
    'IO': [False],
    'GANIMEDES': [False],
    'EUROPA': [False],
}        

# Função que checa se o projeto finalizou
def check_end_project():
    global satelite_lock
    global terraform_completed
    global end_project
    global count
    global mines_stop
    # Apenas uma base acessa os satélites por vez
    with satelite_lock:
        # percorre o dict de terraformação
        for x in terraform_completed.values():
            # Caso algum não tenha terminado, nada acontece
            if (x[0] == False):
                return
        # caso contrário, encerra o projeto
        end_project = True
        count += 1
        # apenas uma base precisa anunciar ao mundo o termino da operação
        if count == 4:
            print('')
            print(f'Operação concluida com sucesso, Duração total: {simulation_time.current_time} anos')
            print(f'Encerrando foguetes restantes...')
            print('')
            # Após o encerramento das bases, as minas podem encerrar
            mines_stop = True

def get_end_project():
    global end_project
    return end_project

def get_bases_locks():
    global bases_locks
    return bases_locks

def get_terraform_completed():
    global terraform_completed
    return terraform_completed

def get_planets_terraform_locks():
    global planets_terraform_locks
    return planets_terraform_locks

def get_planets_pole_locks():
    global planets_pole_locks
    return planets_pole_locks

def get_bases_has_resources():
    global bases_has_resources
    return bases_has_resources

def set_lion_launched(valor):
    global lion_launched
    lion_launched = valor

def get_lion_launched():
    global lion_launched
    return lion_launched

def set_lion_needed(valor):
    global lion_needed 
    lion_needed = valor

def get_lion_needed():
    global lion_needed 
    return lion_needed 

def acquire_lion_production():
    global lion_lock
    lion_lock.acquire()

def release_lion_production():
    global lion_lock
    lion_lock.release()

def acquire_uranium_mine():
    global uranium_mine_acess
    uranium_mine_acess.acquire()

def release_uranium_mine():
    global uranium_mine_acess
    uranium_mine_acess.release()

def acquire_oil_mine():
    global oil_mine_acess
    oil_mine_acess.acquire()

def release_oil_mine():
    global oil_mine_acess
    oil_mine_acess.release()

def acquire_print():
    global mutex_print
    mutex_print.acquire()

def release_print():
    global mutex_print
    mutex_print.release()

def set_planets_ref(all_planets):
    global planets
    planets = all_planets

def get_planets_ref():
    global planets
    return planets

def set_bases_ref(all_bases):
    global bases
    bases = all_bases

def get_bases_ref():
    global bases
    return bases

def set_mines_ref(all_mines):
    global mines
    mines = all_mines

def get_mines_ref():
    global mines
    return mines

def set_release_system():
    global release_system
    release_system = True

def get_release_system():
    global release_system
    return release_system

def set_simulation_time(time):
    global simulation_time
    simulation_time = time

def get_simulation_time():
    global simulation_time
    return simulation_time
