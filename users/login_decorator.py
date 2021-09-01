import json
import jwt

from django.http import JsonResponse

from my_settings  import SECRET_KEY
from users.models import User

def Login_decorator(func):
    def wrapper(self, request, *args, **kwargs):
        try:
            access_token = request.headers.get("Authorization", None)
            payload      = jwt.decode(access_token, SECRET_KEY, algorithm='HS256')
            user         = User.objects.get(id=payload['id'])
            request.user = user

            return func(self, request, *args, **kwargs)
        except jwt.exceptions.DecodeError:
            return JsonResponse({"message" : "INVALID_TOKEN"}, status=400)
        except User.DoesNotExist:
            return JsonResponse({"message" : "INVALID_USER"}, status=400)
        
    return wrapper