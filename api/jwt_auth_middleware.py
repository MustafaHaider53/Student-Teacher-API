import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from channels.db import database_sync_to_async
from urllib.parse import parse_qs

User = get_user_model()

@database_sync_to_async
def get_user_from_token(token):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        user_id = int(payload["user_id"])   
        return User.objects.get(id=user_id)
    except Exception as e:
        return AnonymousUser()    

class JWTAuthMiddleware:
    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):
        scope["user"] = AnonymousUser()
        token = None

        # Try query param
        query_string = parse_qs(scope["query_string"].decode())
        token = query_string.get("token", [None])[0]

        # Try Authorization header
        if not token:
            headers = dict(scope["headers"])
            auth_header = headers.get(b"authorization", None)
            if auth_header:
                try:
                    prefix, token_val = auth_header.decode().split()
                    if prefix.lower() == "bearer":
                        token = token_val
                except ValueError:
                    pass

        # Only set user if token exists
        if token:
            user = await get_user_from_token(token)
            scope["user"] = user

        return await self.inner(scope, receive, send)
