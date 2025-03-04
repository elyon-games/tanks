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
import server.services.storage.main as storage
import common.random 

app: Flask = None 

def Main():
    try :
        global app
        print("Start Server...")
        
        storage.initStorage()
        if not storage.hasKey("key"):
            storage.setValue("key", common.random.generate_random_uuid())
        setConfigParameter("server", "key", storage.getValue("key"))

        config = getConfig("server")
        
        app = Flask(
            f"Elyon Server ({__name__})",
            static_folder=common.path.get_path("server_public"),
            static_url_path="/",
            template_folder=common.path.get_path("server_templates"),
        )
        
        @app.errorhandler(404)
        def page_not_found(error):
            return jsonify({
                "error": True,
                "message": "NO_FOUND",
                "code": 404
            }), 404

        @app.errorhandler(Exception)
        def error_handler(error: Exception) -> tuple[Response, int]:
            error = str(error)
            return jsonify({
                "error": True,
                "message": error if error else "Erreur interne du serveur (LOGIQUE)",
                "code": 500
            }), 500

        @app.errorhandler(500)
        def error_handler(error: HTTPException) -> tuple[Response, int]:
            return jsonify({
                "error": True,
                "message": "Erreur interne du serveur (WEB)",
                "code": 500
            }), 500

        initSessions(app=app)
        initRoute()

        all_files = [
            os.path.join(root, f)
            for root, dirs, files in os.walk(common.path.get_path("src"))
            for f in files
            if common.path.get_path("data") not in root
        ]

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

        process.create_process("server-web", run=start_server_web).start()

        process.create_process("server-clock", run=clock.initClock).start()

        process.create_process("server-cli", run=cmd.initCMD).start()

        process.started_callback("server-main")

        print("Server started")
        print("Bienvenue sur la console server de Elyon Games")
        print("DON'T STOP WITH CTRL+C USE THE COMMAND 'stop'")

        event_stop = process.get_process_running_event("server-web")
        event_stop.wait()
        os.kill(os.getpid(), signal.SIGINT)

    except Exception as e:
        print("Error Fatal in Main Server : ")
        print(e)
        traceback.print_exc()

def initRoute():
    global app
    
    @app.before_request
    def before_request():
        auth_header = request.headers.get('Authorization')
        session['user_id'] = None
        session["auth"] = False
        session["token"] = None
        session["iadmin"] = False

        if auth_header:
            token = auth_header.split(" ")[1]
            user_data = verify_jwt_token(token)
            if user_data:
                session['user_id'] = user_data["user_id"]
                session["auth"] = True
                session["token"] = token
                session["admin"] = user_data["admin"]

    @app.after_request
    def after_request(response):
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("X-Powered-By", "Elyon-Server")
        return response

    app.register_blueprint(route_web)
    app.register_blueprint(route_api, url_prefix="/api")