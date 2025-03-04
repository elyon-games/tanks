import common.process as process
import os
import signal
import time
from server.services.cmd.main import classCMD

class stopCMD(classCMD):
    def __init__(self):
        super().__init__(
            description="Permet de stopper le serveur ! (Attension avec son utilisation)",
            args=[
                {"id": "time", "require": False, "description": "Temps avant l'arrêt du serveur", "type": "int"},
            ]
        )

    def run(self, args=[]):
        time_arg = next((arg["value"] for arg in args if arg["id"] == "time"), None)
        if time_arg is not None:
            for i in range(int(time_arg)):
                print(f"Stopping server in {int(time_arg) - i} seconds...")
                time.sleep(1)
        print("Stopping server...")
        process.stop_all_processes()
        os.kill(os.getpid(), signal.SIGINT)
