from server.services.cmd.base import classCMD
from typing import Dict
import common.process as process
import difflib

comandes: Dict[str, classCMD] = {}

from server.cmd.stop import stopCMD
comandes["stop"] = stopCMD()
from server.cmd.tps import tpsCMD
comandes["tps"] = tpsCMD()
from server.cmd.users_num import users_num
comandes["users:num"] = users_num()

def getCommandMain(command: str):
    return command.split(" ")[0]

def getCommandArgs(command: str, helpCommand: bool = False):
    args = (command.replace(f"{getCommandMain(command)} ", "")).split(" ")
    if args[0] == "": 
        return []
    result = []
    if helpCommand:
        return [{"id": "help", "value": args[0]}]
    for arg in args:
        key_value = arg.split("=")
        if len(key_value) == 2:
            result.append({"id": key_value[0], "value": key_value[1]})
    return result

def initCMD():
    print("Start CLI")
    while process.get_process_running_status("server-cli"):
        command = input("\n")
        commandMain = getCommandMain(command)
        if commandMain == "help":
            commandArgs = getCommandArgs(command, True)
            help_command = commandArgs[0]["value"]
            if help_command == "help":
                print("Utilisation: help <command>")
            else:
                if help_command in comandes:
                    commandData = comandes[help_command]
                    print(f"Description: {commandData.getDescription()}")
                    parameters = commandData.getParameters()
                    if len(parameters) > 0:
                        print("Arguments:")
                        for param in parameters:
                            print(f"  {param}")
                else:
                    print(f"Command '{help_command}' not found.")
        elif commandMain in comandes:
            commandData = comandes[commandMain]
            commandArgs = getCommandArgs(command)
            
            missing_args = commandData.getMissingArgs(commandArgs)
            unknown_args = commandData.getUnknownArgs(commandArgs)

            for arg in unknown_args:
                print(f"Argument inconnu : {arg}")

            for arg in missing_args:
                print(f"Argument manquant : {arg}")
            
            if len(unknown_args) == 0 and len(missing_args) == 0:
                commandData.run(commandArgs)
        else:
            similar_commands = difflib.get_close_matches(command, comandes.keys())
            if similar_commands:
                print(f"Commande introuvable. Voulez-vous dire : {', '.join(similar_commands)} ?")
            else:
                print("Commande introuvable")
    print("Stop CLI")