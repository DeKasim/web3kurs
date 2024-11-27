import logging
from datetime import datetime


logger = logging.getLogger(__name__)


class UserActivityLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Логика перед обработкой запроса
        response = self.get_response(request)
        # Логика после обработки запроса
        self.log_user_activity(request)
        return response

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]
        return request.META.get('REMOTE_ADDR')

    def log_user_activity(self, request):
        ip_address = self.get_client_ip(request)
        user = request.user if request.user.is_authenticated else "Anonymous"
        log_message = f"[{datetime.now()}] User: {user}, IP: {ip_address}, Path: {request.path}, Method: {request.method}"
        logger.info(log_message)
