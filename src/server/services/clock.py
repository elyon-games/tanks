import time
import common.process as process
from common.config import getConfig
from typing import Tuple, List, Callable

# Variables globales
tick_count: int
functions: List[Tuple[Callable, int, int]]
tick_interval: float
start_time: float

functions = []
tick_rate = getConfig("server")["clock"]["tick_rate"]
tick_interval = 1 / tick_rate
tick_count = 0
start_time = time.time()

# Fonction pour obtenir le TPS (Tick Per Second)
def getTPS() -> float:
    global tick_count, start_time
    elapsed_time = time.time() - start_time
    if elapsed_time == 0:
        return 0
    return round(tick_count / elapsed_time, 1)

# Fonction pour obtenir l'intervalle de tick
def getTickInterval() -> float:
    return tick_interval

# Fonction pour obtenir le taux de tick
def getTickRate() -> float:
    return tick_rate

# Fonction pour obtenir le nombre de tick
def getTickCount() -> int:
    return tick_count

# Fonction pour enregistrer une fonction à appeler à chaque tick donné (en tick)
def registerTicked(func: Callable, ticksNum: int) -> None:
    global functions, tick_count
    if ticksNum < 1:
        raise ValueError("TICKS_NUM_INVALID")
    if not callable(func):
        raise ValueError("FUNC_NOT_CALLABLE")
    functions.append((func, ticksNum, 0))

# Fonction pour initialiser l'horloge du serveur
def initClock() -> None:
    print("Start Clock")
    global tick_count, tick_interval, functions, start_time
    start_time = time.time()
    while process.get_process_running_status("server-clock"):
        for i, (func, ticks, last_called_tick) in enumerate(functions):
            if tick_count - last_called_tick >= ticks:
                func()
                functions[i] = (func, ticks, tick_count)
        tick_count += 1
        time.sleep(tick_interval)
    print("Stop Clock")
