import os
import traceback
import signal
import common.path
import common.process as process
from common.config import getConfig, setConfigParameter
from common.args import getArgs
import server.services.clock as clock
import server.services.cmd.main as cmd
from flask import Flask, session, request, jsonify, Response
from werkzeug.exceptions import HTTPException
from server.services.sessions import initSessions
from server.services.tokens import verify_jwt_token
from server.routes.api.main import route_api
from server.routes.web.main import route_web
import server.services.storage as storage
import common.random 
from server.utils import formatErrorRes

app: Flask = None 

# Fonction principale du serveur
def Main():
    try :
        global app
        print("Start Server...")
        
        # Initialisation du stockage
        storage.initStorage()
        # création de la clé du serveur (ID unique du serveur)
        if not storage.hasKey("key"):
            storage.setValue("key", common.random.generate_random_uuid())
        setConfigParameter("server", "key", storage.getValue("key"))

        config = getConfig("server")
        
        # Initialisation du serveur web
        app = Flask(
            f"Elyon Server ({__name__})",
            static_folder=common.path.get_path("server_public"),
            static_url_path="/",
            template_folder=common.path.get_path("server_templates"),
        )
        
        # Gestion des erreurs

        # erreur 404
        @app.errorhandler(404)
        def page_not_found(error):
            return formatErrorRes("NOT_FOUND", "Page non trouvée")

        # erreur 500 (interne)
        @app.errorhandler(Exception)
        def error_handler(error: Exception) -> tuple[Response, int]:
            print("Erreur interne du serveur", error)
            traceback.print_exc()
            return formatErrorRes("INTERNAL_SERVER_ERROR", f"Erreur interne du serveur (LOGIQUE) {str(error)}")

        # erreur 500 (web)
        @app.errorhandler(500)
        def error_handler(error: HTTPException) -> tuple[Response, int]:
            return formatErrorRes("INTERNAL_SERVER_ERROR", "Erreur interne du serveur (WEB)")

        # Initialisation des sessions
        initSessions(app=app)

        # Initialisation des routes
        initRoute()

        # liste de tous les fichiers du serveur
        all_files = [
            os.path.join(root, f)
            for root, dirs, files in os.walk(common.path.get_path("src"))
            for f in files
            if common.path.get_path("data") not in root
        ]

        # fonction pour démarrer le serveur web en fonction du mode (optimisé ou natif)
        def start_server_web():
            if config["web"]["mode"] == "optimized":
                from waitress import serve
                serve(app=app,
                    host=config["host"],
                    port=config["port"]
                )
            elif config["web"]["mode"] == "native":
                app.run(
                    host=config["host"],
                    port=config["port"],
                    debug=config["debug"],
                    extra_files=all_files,
                    threaded=True
                )

        # démarrage des processus
        # processur du serveur principal
        process.create_process("server-web", run=start_server_web).start()

        # processus de l'horloge
        process.create_process("server-clock", run=clock.initClock).start()

        # processus de la console
        process.create_process("server-cli", run=cmd.initCMD).start()

        # processus du serveur principal
        process.started_callback("server-main")

        print("Server started")
        print("Bienvenue sur la console server de Elyon Tanks")
        print("DON'T STOP WITH CTRL+C USE THE COMMAND 'stop'")

        # attente de l'arrêt du processus et gestion de l'arrêt du serveur
        event_stop = process.get_process_running_event("server-web")
        event_stop.wait()
        os.kill(os.getpid(), signal.SIGINT)

    except Exception as e:
        # gestion des erreurs fatales
        print("Error Fatal in Main Server : ")
        print(e)
        traceback.print_exc()

def initRoute():
    global app

    # fonction qui gère les requêtes après le traitement
    @app.after_request
    def after_request(response):
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("X-Powered-By", "Elyon-Server")
        return response

    # enregistrement des routes
    app.register_blueprint(route_web)
    app.register_blueprint(route_api, url_prefix="/api")