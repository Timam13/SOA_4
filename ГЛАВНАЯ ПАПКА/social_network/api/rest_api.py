"""
REST API для социальной сети и платформы программ лояльности.
"""

from flask import Flask, request, jsonify
from grpc import insecure_channel
import os
import datetime
import logging

import os
import sys

# путь к директории с proto-файлами в sys.path
proto_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'proto')
if proto_dir not in sys.path:
    sys.path.append(proto_dir)

import service_pb2
import service_pb2_grpc

# логи
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

GRPC_SERVER = os.environ.get('GRPC_SERVER', 'localhost:50051')

@app.route("/", methods=["GET"])
def health_check():
    return jsonify({"status": "ok", "service": "social-network-api"})

@app.route("/get_post", methods=["POST"])
def get_post():
    data = request.get_json() or {}
    client_id = data.get("client_id")
    post_id = data.get("post_id")
    
    if not client_id or not post_id:
        return jsonify({"error": "client_id и post_id обязательны"}), 400
    
    try:
        with insecure_channel(GRPC_SERVER) as channel:
            stub = service_pb2_grpc.SocialNetworkStub(channel)
            response = stub.GetPost(service_pb2.GetPostRequest(
                client_id=client_id,
                post_id=post_id
            ))
        
        return jsonify({"post_content": response.post_content})
    except Exception as e:
        logger.error(f"Ошибка при запросе к gRPC серверу: {e}")
        return jsonify({"error": "Ошибка сервера"}), 500



@app.route("/create_comment", methods=["POST"])
def create_comment():
    data = request.get_json() or {}
    client_id = data.get("client_id")
    post_id = data.get("post_id")
    comment_text = data.get("comment_text")

    if not client_id or not post_id or not comment_text:
        return jsonify({"error": "client_id, post_id и comment_text обязательны"}), 400
    
    try:
        with insecure_channel(GRPC_SERVER) as channel:
            stub = service_pb2_grpc.SocialNetworkStub(channel)
            response = stub.CreateComment(service_pb2.CreateCommentRequest(
                client_id=client_id,
                post_id=post_id,
                comment_text=comment_text
            ))
        
        return jsonify({"status": response.status})
    except Exception as e:
        logger.error(f"Ошибка при запросе к gRPC серверу: {e}")
        return jsonify({"error": "Ошибка сервера"}), 500

@app.route("/get_comments", methods=["GET"])
def get_comments():
    # пагинация
    post_id = request.args.get("post_id")
    page = int(request.args.get("page", 1))
    page_size = int(request.args.get("page_size", 10))

    if not post_id:
        return jsonify({"error": "post_id обязателен"}), 400
    
    try:
        with insecure_channel(GRPC_SERVER) as channel:
            stub = service_pb2_grpc.SocialNetworkStub(channel)
            response = stub.GetComments(service_pb2.GetCommentsRequest(
                post_id=post_id,
                page=page,
                page_size=page_size
            ))
        
        # Преобразуем комментарии в JSON
        comments = []
        for comment in response.comments:
            comments.append({
                "client_id": comment.client_id,
                "text": comment.text,
                "timestamp": comment.timestamp
            })
        
        return jsonify({
            "comments": comments,
            "total_count": response.total_count,
            "page": response.page,
            "page_size": response.page_size
        })
    except Exception as e:
        logger.error(f"Ошибка при запросе к gRPC серверу: {e}")
        return jsonify({"error": "Ошибка сервера"}), 500

@app.route("/register", methods=["POST"])
def register_client():
    data = request.get_json() or {}
    client_id = data.get("client_id")

    if not client_id:
        return jsonify({"error": "client_id обязателен"}), 400
    
    try:
        with insecure_channel(GRPC_SERVER) as channel:
            stub = service_pb2_grpc.SocialNetworkStub(channel)
            response = stub.RegisterClient(service_pb2.RegisterClientRequest(
                client_id=client_id,
                registration_date=datetime.datetime.utcnow().isoformat()
            ))
        
        return jsonify({"status": response.status})
    except Exception as e:
        logger.error(f"Ошибка при запросе к gRPC серверу: {e}")
        return jsonify({"error": "Ошибка сервера"}), 500

@app.route("/get_promocode", methods=["POST"])
def get_promocode():
    data = request.get_json() or {}
    client_id = data.get("client_id")
    promocode_id = data.get("promocode_id")
    
    if not client_id or not promocode_id:
        return jsonify({"error": "client_id и promocode_id обязательны"}), 400
    
    try:
        with insecure_channel(GRPC_SERVER) as channel:
            stub = service_pb2_grpc.SocialNetworkStub(channel)
            response = stub.GetPromocode(service_pb2.GetPromocodeRequest(
                client_id=client_id,
                promocode_id=promocode_id
            ))
        
        return jsonify({"promocode_content": response.promocode_content})
    except Exception as e:
        logger.error(f"Ошибка при запросе к gRPC серверу: {e}")
        return jsonify({"error": "Ошибка сервера"}), 500

@app.route("/click_promocode", methods=["POST"])
def click_promocode():
    data = request.get_json() or {}
    client_id = data.get("client_id")
    promocode_id = data.get("promocode_id")
    
    if not client_id or not promocode_id:
        return jsonify({"error": "client_id и promocode_id обязательны"}), 400
    
    try:
        with insecure_channel(GRPC_SERVER) as channel:
            stub = service_pb2_grpc.SocialNetworkStub(channel)
            response = stub.ClickPromocode(service_pb2.ClickPromocodeRequest(
                client_id=client_id,
                promocode_id=promocode_id
            ))
        
        return jsonify({"status": response.status})
    except Exception as e:
        logger.error(f"Ошибка при запросе к gRPC серверу: {e}")
        return jsonify({"error": "Ошибка сервера"}), 500

@app.route("/create_promocode_comment", methods=["POST"])
def create_promocode_comment():
    data = request.get_json() or {}
    client_id = data.get("client_id")
    promocode_id = data.get("promocode_id")
    comment_text = data.get("comment_text")
    
    if not client_id or not promocode_id or not comment_text:
        return jsonify({"error": "client_id, promocode_id и comment_text обязательны"}), 400
    
    try:
        with insecure_channel(GRPC_SERVER) as channel:
            stub = service_pb2_grpc.SocialNetworkStub(channel)
            response = stub.CreatePromocodeComment(service_pb2.CreatePromocodeCommentRequest(
                client_id=client_id,
                promocode_id=promocode_id,
                comment_text=comment_text
            ))
        
        return jsonify({"status": response.status})
    except Exception as e:
        logger.error(f"Ошибка при запросе к gRPC серверу: {e}")
        return jsonify({"error": "Ошибка сервера"}), 500

@app.route("/get_promocode_comments", methods=["GET"])
def get_promocode_comments():
    # пагинация
    promocode_id = request.args.get("promocode_id")
    page = int(request.args.get("page", 1))
    page_size = int(request.args.get("page_size", 10))
    
    if not promocode_id:
        return jsonify({"error": "promocode_id обязателен"}), 400
    
    try:
        with insecure_channel(GRPC_SERVER) as channel:
            stub = service_pb2_grpc.SocialNetworkStub(channel)
            response = stub.GetPromocodeComments(service_pb2.GetPromocodeCommentsRequest(
                promocode_id=promocode_id,
                page=page,
                page_size=page_size
            ))
        
        # Преобразуем комментарии в JSON
        comments = []
        for comment in response.comments:
            comments.append({
                "client_id": comment.client_id,
                "text": comment.text,
                "timestamp": comment.timestamp
            })
        
        return jsonify({
            "comments": comments,
            "total_count": response.total_count,
            "page": response.page,
            "page_size": response.page_size
        })
    except Exception as e:
        logger.error(f"Ошибка при запросе к gRPC серверу: {e}")
        return jsonify({"error": "Ошибка сервера"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
