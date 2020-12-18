import json
import re
import bcrypt
import jwt

from django.http      import JsonResponse, HttpResponse
from django.views     import View
from django.db.models import Q

from users.models     import User
from my_settings      import SECRET_KEY, JWT_ALGORITHM
from users.utils      import LoginConfirm, is_valid, \
                             PW_REGEX, EMAIL_REGEX, NICKNAME_REGEX

class SignupView(View): 
    def post(self,request):
        try:
            data = json.loads(request.body)

            if not is_valid(data['email'],EMAIL_REGEX):
                return JsonResponse({"MESSAGE":"INVALID_EMAIL_FORMAT"},status=400)
            
            if not is_valid(data['password'],PW_REGEX):
                return JsonResponse({"MESSAGE":"INVALID_PW_FORMAT"},status=400)
                
            if not is_valid(data['nickname'],NICKNAME_REGEX):
                return JsonResponse({"MESSAGE":"INVALID_NICKNAME_FORMAT"},status=400)
        
            if User.objects.filter(Q(email=data['email'])|Q(nickname=data['nickname'])).exists():
            
                return JsonResponse({"MESSAGE":"USER_ALREADY_EXISTS"},status=400)
                
            hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'),bcrypt.gensalt())
            
            User.objects.create(
                nickname = data['nickname'],
                email    = data["email"],
                password = hashed_password.decode()
            )
            
            return HttpResponse(status=201)

        except KeyError:
            return JsonResponse({'MESSAGE':"KEY_ERROR"},status=400)
        
        except json.JSONDecodeError:
            return JsonResponse({"MESSAGE":"INVALID_DATA"},status=400)
    
class SigninView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            user = User.objects.get(email=data['email'])
            
            if not bcrypt.checkpw(data['password'].encode(),user.password.encode()):
                return JsonResponse({"MESSAGE":"INVALID_USER"},status=400) 
            
            access_token = jwt.encode({"id":user.id},SECRET_KEY,algorithm=JWT_ALGORITHM)
            
            return JsonResponse({"NICKNAME":user.nickname,"ACCESS_TOKEN":access_token.decode()},status=200)

        except KeyError:
            return JsonResponse({'MESSAGE':"KEY_ERROR"},status=400)

        except User.DoesNotExist:
            return JsonResponse({'MESSAGE':"INVALID_USER"},status=401)

        except json.JSONDecodeError:
            return JsonResponse({"MESSAGE":"INVALID_DATA"},status=400)
