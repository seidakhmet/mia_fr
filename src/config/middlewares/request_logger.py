
"""
Middleware to log `*/api/*` requests and responses.
"""
import socket
import time
import json
import logging
from django.utils.translation import gettext_lazy as _


request_logger = logging.getLogger("django.request")

class RequestLogMiddleware:
    """Request Logging Middleware."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.time()
        username = request.user.username if request.user.id else "Anonymous"
        try:
            request_body = request.body.decode("utf-8") if request.body else {}
        except Exception:
            request_body = {}

        log_data = {
            "remote_address": request.META["REMOTE_ADDR"],
            "server_hostname": socket.gethostname(),
            "request_method": request.method,
            "request_path": request.get_full_path(),
            "username": username,
            "request_body": request_body
        }
        # request passes on to controller
        response = self.get_response(request)

        log_data["run_time"] = time.time() - start_time

        request_logger.info(msg=log_data, extra={"username": username})

        return response

    # Log unhandled exceptions as well
    def process_exception(self, request, exception):
        try:
            raise exception
        except Exception as e:
            request_logger.exception("Unhandled Exception: " + str(e))
        return exception
