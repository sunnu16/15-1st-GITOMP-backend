import jwt
import json
import re

from users.models     import User
from django.db.models import Q
from my_settings      import SECRET_KEY,JWT_ALGORITHM
from django.http      import JsonResponse

def validate_email(text):
    EMAIL_REGEX    = '^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.compile(EMAIL_REGEX).match(text)

def validate_password(text):
    PW_REGEX       = '^[A-Za-z0-9~`!@#$%\^&*()-+=]{8,256}$' 
    return re.compile(PW_REGEX).match(text)

def validate_nickname(text):
    NICKNAME_REGEX = '^[A-Za-z0-9ㄱ-힣~`!@#$%\^&*()-+=]{3,16}$'
    return re.compile(NICKNAME_REGEX).match(text)

def LoginConfirm(original_function):
    def wrapper(self, request, *args, **kwargs):
        token = request.headers.get("Authorization", None)
        try:
            if token:
                token_payload = jwt.decode(token, SECRET_KEY, algorithms=JWT_ALGORITHM)
                user          = User.objects.get(id=token_payload['id'])
                request.user  = user
                return original_function(self, request, *args, **kwargs)

            return JsonResponse({'messaege':'NEED_LOGIN'}, status=401)

        except jwt.ExpiredSignatureError:
            return JsonResponse({'message':'EXPIRED_TOKEN'}, status=401)

        except jwt.DecodeError:
            return JsonResponse({'message':'INVALID_DATA'}, status=401)

        except Users.DoesNotExist:
            return JsonResponse({'message':'INVALID_USER'}, status=401)
    return wrapper

def validate_signup(original_function):
    def wrapper(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            request.email = data['email']
            request.password = data['password']
            request.nickname = data['nickname']
            
            if not validate_email(request.email):
                return JsonResponse({"MESSAGE":"INVALID_EMAIL"},status=400)
            
            if not validate_password(request.password):
                return JsonResponse({"MESSAGE":"INVALID_PASSWORD"},status=400)
            
            if not validate_nickname(request.nickname):
                return JsonResponse({"MESSAGE":"INVALID_NICKNAME"},status=400)
            
            if User.objects.filter(Q(nickname=request.nickname)|Q(email=request.email)).exists():
                return JsonResponse({"MESSAGE":"INVALID_USER"},status=400)

            return original_function(self, request, *args, **kwargs)

        except KeyError:
            return JsonResponse({'MESSAGE':'KEY_ERROR'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({"MESSAGE","INVALID_DATA"},status=400)
    
    return wrapper


