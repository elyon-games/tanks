import time
import common.process as process
from common.config import getConfig
from typing import Tuple, List, Callable

tick_count: int
functions: List[Tuple[Callable, int, int]]
tick_interval: float
start_time: float

functions = []
tick_rate = getConfig("server")["clock"]["tick_rate"]
tick_interval = 1 / tick_rate
tick_count = 0
start_time = time.time()

def getTPS() -> float:
    global tick_count, start_time
    elapsed_time = time.time() - start_time
    if elapsed_time == 0:
        return 0
    return round(tick_count / elapsed_time, 1)

def getTickInterval() -> float:
    return tick_interval

def getTickRate() -> float:
    return tick_rate

def getTickCount() -> int:
    return tick_count

def registerTicked(func: Callable, ticksNum: int) -> None:
    print(func)
    global functions, tick_count
    if ticksNum < 1:
        raise ValueError("TICKS_NUM_INVALID")
    if not callable(func):
        raise ValueError("FUNC_NOT_CALLABLE")
    functions.append((func, ticksNum, 0))

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
