
import threading

request_count = 0
lock = threading.Lock()

def print_request_count():
    global request_count
    with lock:
        request_count += 1
        print(f"Total API Requests: {request_count}")

class RequestCounterMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/admin/'):  
            print_request_count()
        return self.get_response(request)
