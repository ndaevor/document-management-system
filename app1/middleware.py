from django.conf import settings
from django.contrib.sessions.middleware import SessionMiddleware
from django.utils.deprecation import MiddlewareMixin

class AdminSessionMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.path.startswith('/admin/'):
            session_key = request.COOKIES.get(settings.ADMIN_SESSION_COOKIE_NAME)
            if session_key:
                request.session = self.get_session_store(session_key)
            else:
                request.session = self.get_session_store(None)
        else:
            session_key = request.COOKIES.get(settings.USER_SESSION_COOKIE_NAME)
            if session_key:
                request.session = self.get_session_store(session_key)
            else:
                request.session = self.get_session_store(None)

    def process_response(self, request, response):
        if request.path.startswith('/admin/'):
            if request.session.session_key:
                response.set_cookie(settings.ADMIN_SESSION_COOKIE_NAME, request.session.session_key)
        else:
            if request.session.session_key:
                response.set_cookie(settings.USER_SESSION_COOKIE_NAME, request.session.session_key)
        return response

    def get_session_store(self, session_key):
        from importlib import import_module
        engine = import_module(settings.SESSION_ENGINE)
        return engine.SessionStore(session_key)
