from flask import Blueprint, request, session, jsonify
import server.services.network.main as network
from server.middleware.auth import login_required
from server.utils import formatRes, formatErrorRes
from server.services.network.gateways import Gateway
from typing import Optional
from server.services.clock import registerTicked
from common.time import get_current_time_ms

route_client_gateway = Blueprint("api-client-gateway", __name__)

@route_client_gateway.before_request
def before_request():
    body: dict = request.get_json(silent=True)
    if not body:
        session["gateway"] = None
        return
    
    id = body.get("gateway_id", None)
    key = body.get("gateway_key", None)
    if id and key:
        gateway = network.get_gateway(id)
        if gateway and gateway.verify_key(key):
            session["gateway"] = gateway
        else:
            session["gateway"] = None

@route_client_gateway.route("/update", methods=["POST"])
def update_gateway():
    gateway: Optional[Gateway] = session.get("gateway")
    if gateway:
        gateway.update()
        return formatRes("UPDATED", {
            "packet_count": len(gateway.packets),
            "groups": gateway.groups,
            "packets": gateway.get_messages("server-to-client"),
            "status": gateway.status,
            "last_update": gateway.last_update
        })
    else:
        return formatErrorRes("GATEWAY_NOT_FOUND", "Gateway not found")

@route_client_gateway.route("/send", methods=["POST"])
def send_message():
    gateway: Optional[Gateway] = session.get("gateway")
    if gateway:
        body: dict = request.get_json(silent=True)
        if not body:
            return formatErrorRes("INVALID_BODY", "Invalid body")
        
        message = body.get("message", None)
        if not message:
            return formatErrorRes("INVALID_MESSAGE", "Invalid message")
        
        gateway.send_message(message)
        return formatRes("SENT", {})
    else:
        return formatErrorRes("GATEWAY_NOT_FOUND", "Gateway not found")


@route_client_gateway.route("/connect", methods=["POST"])
def connect_gateway():
    gateway: Optional[Gateway] = session.get("gateway")
    if gateway:
        gateway.connect()
        print(f"Gateway {gateway.id} connected by user {gateway.userID}")
        return formatRes("CONNECTED", {})
    else:
        return formatErrorRes("GATEWAY_NOT_FOUND", "Gateway not found")

@route_client_gateway.route("/close", methods=["POST"])
def close_gateway():
    gateway: Optional[Gateway] = session.get("gateway")
    if gateway:
        gateway.close()
        return formatRes("CLOSED", {})
    else:
        return formatErrorRes("GATEWAY_NOT_FOUND", "Gateway not found")

def verify_gateway():
    for gateway in network.gateways:
        if gateway.is_expired():
            print(f"Gateway {gateway.id} is expired")
            gateway.close()

        if gateway.status == "close" and gateway.last_update + 10000 < get_current_time_ms():
            network.gateways.remove(gateway)
            print(f"Gateway {gateway.id} is deleted")

registerTicked(verify_gateway, 150)