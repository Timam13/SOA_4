import grpc
import datetime
import logging
from concurrent import futures

import os
import sys

# путь к директории с proto-файлами в sys.path
proto_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'proto')
if proto_dir not in sys.path:
    sys.path.append(proto_dir)

import service_pb2
import service_pb2_grpc

from social_network.core.kafka_producer import send

# логи
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Имитация базы данных для хранения комментариев
post_comments_db = {}  # {post_id: [{"client_id": "...", "text": "...", "timestamp": "..."}]}
promocode_comments_db = {}  # {promocode_id: [{"client_id": "...", "text": "...", "timestamp": "..."}]}

class SocialNetworkService(service_pb2_grpc.SocialNetworkServicer):
    def GetPost(self, request, context):
        post_id = request.post_id
        
        # Отправляем в Kafka
        send("post_views", {
            "client_id": request.client_id,
            "post_id": post_id,
            "action": "view",
            "timestamp": datetime.datetime.utcnow().isoformat()
        })
        
        # Возвращаем содержимое поста
        return service_pb2.GetPostResponse(post_content=f"Содержимое поста {post_id}")
    

    
    def CreateComment(self, request, context):
        post_id = request.post_id
        comment_text = request.comment_text
        client_id = request.client_id
        timestamp = datetime.datetime.utcnow().isoformat()
        
        # Сохраняем комментарий
        if post_id not in post_comments_db:
            post_comments_db[post_id] = []
        
        post_comments_db[post_id].append({
            "client_id": client_id,
            "text": comment_text,
            "timestamp": timestamp
        })
        
        # Отправляем в Kafka
        send("post_comments", {
            "client_id": client_id,
            "post_id": post_id,
            "action": "comment",
            "comment_text": comment_text,
            "timestamp": timestamp
        })
        
        return service_pb2.CreateCommentResponse(status="comment_created")
    
    def GetComments(self, request, context):
        post_id = request.post_id
        page = request.page if request.page > 0 else 1
        page_size = request.page_size if request.page_size > 0 else 10
        
        comments = post_comments_db.get(post_id, [])
        total_count = len(comments)
        
        # Применяем пагинацию
        start_idx = (page - 1) * page_size
        end_idx = start_idx + page_size
        paginated_comments = comments[start_idx:end_idx]
        
        # ответ
        response_comments = []
        for comment in paginated_comments:
            response_comments.append(service_pb2.Comment(
                client_id=comment["client_id"],
                text=comment["text"],
                timestamp=comment["timestamp"]
            ))
        
        return service_pb2.GetCommentsResponse(
            comments=response_comments,
            total_count=total_count,
            page=page,
            page_size=page_size
        )
    
    def RegisterClient(self, request, context):
        client_id = request.client_id
        registration_date = request.registration_date
        
        send("client_registration", {
            "client_id": client_id,
            "registration_date": registration_date
        })
        
        return service_pb2.RegisterClientResponse(status="registered")
    
    # лояльность
    def GetPromocode(self, request, context):
        promocode_id = request.promocode_id
        
        send("promocode_views", {
            "client_id": request.client_id,
            "promocode_id": promocode_id,
            "action": "view",
            "timestamp": datetime.datetime.utcnow().isoformat()
        })
        
        return service_pb2.GetPromocodeResponse(promocode_content=f"Промокод {promocode_id}: SALE50")
    
    def ClickPromocode(self, request, context):
        promocode_id = request.promocode_id

        send("promocode_clicks", {
            "client_id": request.client_id,
            "promocode_id": promocode_id,
            "action": "click",
            "timestamp": datetime.datetime.utcnow().isoformat()
        })
        
        return service_pb2.ClickPromocodeResponse(status="clicked")
    
    def CreatePromocodeComment(self, request, context):
        promocode_id = request.promocode_id
        comment_text = request.comment_text
        client_id = request.client_id
        timestamp = datetime.datetime.utcnow().isoformat()
        
        if promocode_id not in promocode_comments_db:
            promocode_comments_db[promocode_id] = []
        
        promocode_comments_db[promocode_id].append({
            "client_id": client_id,
            "text": comment_text,
            "timestamp": timestamp
        })

        send("promocode_comments", {
            "client_id": client_id,
            "promocode_id": promocode_id,
            "action": "comment",
            "comment_text": comment_text,
            "timestamp": timestamp
        })
        
        return service_pb2.CreatePromocodeCommentResponse(status="comment_created")
    
    def GetPromocodeComments(self, request, context):
        promocode_id = request.promocode_id
        page = request.page if request.page > 0 else 1
        page_size = request.page_size if request.page_size > 0 else 10
        
        # Получаем комментарии
        comments = promocode_comments_db.get(promocode_id, [])
        total_count = len(comments)
        
        # Применяем пагинацию
        start_idx = (page - 1) * page_size
        end_idx = start_idx + page_size
        paginated_comments = comments[start_idx:end_idx]
        
        response_comments = []
        for comment in paginated_comments:
            response_comments.append(service_pb2.PromocodeComment(
                client_id=comment["client_id"],
                text=comment["text"],
                timestamp=comment["timestamp"]
            ))
        
        return service_pb2.GetPromocodeCommentsResponse(
            comments=response_comments,
            total_count=total_count,
            page=page,
            page_size=page_size
        )

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=4))
    service_pb2_grpc.add_SocialNetworkServicer_to_server(
        SocialNetworkService(), server
    )
    server.add_insecure_port("[::]:50051")
    server.start()
    logger.info("gRPC сервер запущен на порту 50051")
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
