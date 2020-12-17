import jwt
import json
import re

from users.models import User
from my_settings  import SECRET_KEY,JWT_ALGORITHM
from django.http  import JsonResponse

PW_REGEX       = '^[A-Za-z0-9~`!@#$%\^&*()-+=]{8,256}$'
EMAIL_REGEX    = '^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
NICKNAME_REGEX = '^[A-Za-z0-9ㄱ-힣~`!@#$%\^&*()-+=]{3,16}$'

def is_valid(text, regex):
    return re.compile(regex).match(text)

class LoginConfirm:
    def __init__(self, original_function):
        self.original_function = original_function

    def __call__(self, request, *args, **kwargs):
        token = request.headers.get("Authorization", None)
        try:
            if token:
                token_payload = jwt.decode(token, SECRET_KEY, algorithms=JWT_ALGORITHM)
                user          = User.objects.get(id=token_payload['id'])
                request.user  = user
                return self.original_function(self, request, *args, **kwargs)

            return JsonResponse({'messaege':'NEED_LOGIN'}, status=401)

        except jwt.ExpiredSignatureError:
            return JsonResponse({'message':'EXPIRED_TOKEN'}, status=401)

        except jwt.DecodeError:
            return JsonResponse({'message':'INVALID_DATA'}, status=401)

        except Users.DoesNotExist:
            return JsonResponse({'message':'INVALID_USER'}, status=401)
