
import threading
import logging 

request_count = 0
lock = threading.Lock()
logger = logging.getLogger('request_counter') 

class RequestCounterMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        global request_count 
        with lock: 
            request_count += 1
            logger.info(f"Total API Requests: {request_count}")
        response = self.get_response(request)
        return response 