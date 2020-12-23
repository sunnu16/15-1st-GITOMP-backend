import json
import re
import bcrypt
import jwt

from django.http      import JsonResponse, HttpResponse
from django.views     import View

from users.models     import User
from my_settings      import SECRET_KEY, JWT_ALGORITHM
from users.utils      import LoginConfirm, validate_signup

class SignupView(View): 
    @validate_signup
    def post(self,request):
            
        hashed_password = bcrypt.hashpw(request.password.encode('utf-8'),bcrypt.gensalt())
            
        User.objects.create(
            nickname = request.nickname,
            email    = request.email,
            password = hashed_password.decode()
        )
        
        return HttpResponse(status=201)

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
