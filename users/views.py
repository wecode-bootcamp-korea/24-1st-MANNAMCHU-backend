import json
import re
import bcrypt
import jwt

from my_settings     import SECRET_KEY
from django.views    import View
from django.http     import JsonResponse
from django.db.utils import DataError

from users.models import User

class SignUp(View):
    def post(self ,request):
        data = json.loads(request.body)
        email_format       = re.compile('\w+[@]\w+[.]\w+')
        password_format    = re.compile('^(?=.*[a-zA-Z])(?=.*[0-9])(?=.*[!@#$%^&*])[a-zA-Z0-9!@#$%^&*]{8,20}$')

        try:
            if not email_format.search(data['email']):
                return JsonResponse({"message" : "INVALID_EMAIL_FORMAT"}, status=400)

            if not password_format.match(data['password']):
                return JsonResponse({"message" : "INVALID_PASSWORD_FORMAT"}, status=400)

            if User.objects.filter(email=data['email']).exists():
                return JsonResponse({"message" : "SAME_EMAIL_EXISTS"}, status=400)

            salt            = bcrypt.gensalt()
            encode_password = data['password'].encode('utf-8')
            hash_password   = bcrypt.hashpw(encode_password, salt)
            decode_password = hash_password.decode('utf-8')

            User.objects.create(
                name     = data['name'],
                password = decode_password,
                email    = data['email'],
                phone    = data['phone'],
                address  = data['address'],
            )
            return JsonResponse({"message" : "SUCCESS"}, status=200)
        except KeyError:
            return JsonResponse({"message" : "KEY_ERROR"}, status=400)
        except DataError:
            return JsonResponse({"message" : "TOO_LONG"}, status=400)

class SignIn(View):
    def post(self, request):
        data = json.loads(request.body)
        try:
            if not User.objects.filter(email=data['email']).exists():
                return JsonResponse({"message" : "INVALID_USER"}, status=401)
            
            user = User.objects.get(email=data['email'])

            if not bcrypt.checkpw(data['password'].encode('utf-8'), user.password.encode('utf-8')):
                return JsonResponse({"mesaage" : "INVALID_PASSWORD"}, status=401)
            
            token = jwt.encode({"user_id" : user.id}, SECRET_KEY, algorithm='HS256')

            return JsonResponse({"message" : "SUCCESS", "token" : token}, status=200)
        except KeyError:
            return JsonResponse({"message" : "KEY_ERROR"}, status=400)