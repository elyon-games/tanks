import common.utils
import common.path
import shutil

# fonction pour créer un dossier de données s'il n'existe pas
def create_data(folder_name: str) -> None:
    try:
        common.utils.create_folder_if_not_exists(common.path.get_path(folder_name))
    except PermissionError as e:
        print(f"Erreur de permission lors de la création de '{folder_name}' : {e}")
    except Exception as e:
        print(f"Une erreur imprévue est survenue lors de la création de '{folder_name}' : {e}")

# fonction pour supprimer un dossier de données
def clear_data(folder_name: str) -> None:
    try:
        shutil.rmtree(common.path.get_path(folder_name))
    except FileNotFoundError:
        print(f"Le dossier '{folder_name}' n'existe pas.")
    except PermissionError as e:
        print(f"Erreur de permission lors de la suppression de '{folder_name}' : {e}")
    except Exception as e:
        print(f"Une erreur imprévue est survenue lors de la suppression de '{folder_name}' : {e}")

# fonction pour créer un dossier de données pour le serveur
def createServerData() -> None:
    create_data("server_data")
    create_data("server_files")
    create_data("server_database")
    create_data("server_sessions")
    create_data("server_files")

# fonction pour créer un dossier de données pour le client
def createClientData() -> None:
    create_data("client_data")

# fonction pour créer un dossier de données 
def createDataFolder() -> None:
    create_data("data")
    create_data("logs")

# fonction pour supprimer tous les dossiers de données
def clearAllData() -> None:
    clear_data("data")

# fonction pour supprimer les données du serveur
def clearServerData() -> None:
    clear_data("server_data")

# fonction pour supprimer les données du client
def clearClientData() -> None:
    clear_data("client_data")
