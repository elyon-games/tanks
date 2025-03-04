import threading
from typing import Callable, Dict, Optional, Any

process: Dict[int, 'Process'] = {}

class Process:
    def __init__(self, id: int, run: Callable, startCallback: Optional[Callable[[], None]] = None, stopCallback: Optional[Callable[[], None]] = None, *args: Any, **kwargs: Any) -> None:
        self.id = id
        self.run = run
        self.startCallback = startCallback
        self.stopCallback = stopCallback
        self.thread = threading.Thread(target=self.run, args=args, kwargs=kwargs)
        self._stop_event = threading.Event()
        self._started = False

    def start(self) -> None:
        if self._started:
            raise RuntimeError("PROCESS_ALREADY_STARTED")
        self._started = True
        self.thread.start()
        if self.startCallback:
            self.startCallback()

    def stop(self) -> None:
        self._stop_event.set()
        self._started = False
        if self.stopCallback:
            self.stopCallback()

    def is_stopped(self) -> bool:
        return self._stop_event.is_set()

def create_process(id: int, run: Callable, startCallback: Optional[Callable[[], None]] = None, stopCallback: Optional[Callable[[], None]] = None, *args: Any, **kwargs: Any) -> Process:
    if id in process:
        raise ValueError("PROCESS_INVALID_ID")
    new_process = Process(id, run, startCallback, stopCallback, *args, **kwargs)
    process[id] = new_process
    return new_process

def get_process(id: int) -> Process:
    if id not in process:
        raise ValueError("PROCESS_INVALID_ID")
    return process[id]

def remove_process(id: int) -> None:
    if id not in process:
        raise ValueError("PROCESS_INVALID_ID")
    del process[id]

def get_all_processes() -> Dict[int, Process]:
    return process

def start_process(id: int) -> None:
    if id not in process:
        raise ValueError("PROCESS_INVALID_ID")
    process[id].start()

def start_all_processes() -> None:
    for id in process:
        process[id].start()

def stop_all_processes() -> None:
    print("stopping all processes")
    for id in process:
        process[id].stop()

def stop_process(id: int) -> None:
    print("stopping process")
    if id not in process:
        raise ValueError("PROCESS_INVALID_ID")
    process[id].stop()

def restart_process(id: int) -> None:
    if id not in process:
        raise ValueError("PROCESS_INVALID_ID")
    process[id].stop()
    process[id].start()

def restart_all_processes() -> None:
    for id in process:
        process[id].stop()
        process[id].start()

def started_callback(id: int) -> None:
    if id not in process:
        raise ValueError("PROCESS_INVALID_ID")
    if process[id].startCallback is not None:
        process[id].startCallback()

def set_started_callback(id: int, callback: Callable[[], None]) -> None:
    if id not in process:
        raise ValueError("PROCESS_INVALID_ID")
    process[id].startCallback = callback

def stopped_callback(id: int) -> None:
    if id not in process:
        raise ValueError("PROCESS_INVALID_ID")
    if process[id].stopCallback is not None:
        process[id].stopCallback()

def set_stopped_callback(id: int, callback: Callable[[], None]) -> None:
    if id not in process:
        raise ValueError("PROCESS_INVALID_ID")
    process[id].stopCallback = callback

def started_callback_all() -> None:
    for id in process:
        started_callback(id)

def stopped_callback_all() -> None:
    for id in process:
        stopped_callback(id)

def get_process_running_status(id: int) -> bool:
    if id not in process:
        raise ValueError("PROCESS_INVALID_ID")
    return not process[id].is_stopped()

def get_process_running_event(id: int) -> threading.Event:
    if id not in process:
        raise ValueError("PROCESS_INVALID_ID")
    return process[id]._stop_event