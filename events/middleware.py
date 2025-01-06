from django.utils.deprecation import MiddlewareMixin

class APICallTrackerMiddleware(MiddlewareMixin):
    def process_request(self, request):
        session = request.session
        session['api_call_count'] = session.get('api_call_count', 0) + 1
        session.save()
