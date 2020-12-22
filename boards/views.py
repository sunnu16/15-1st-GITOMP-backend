import json
import math

from django.http      import JsonResponse,HttpResponse
from django.views     import View
from boards.models    import Board,BoardCategory,Comment
from users.models     import User
from django.db.models import Q

from users.utils      import LoginConfirm

class BoardView(View):
    def get(self, request):

        query       = Q()
        page        = int(request.GET.get('page',1))
        BOARD_COUNT = 10
        limit       = BOARD_COUNT*page
        offset      = limit-BOARD_COUNT

        search_string = request.GET.get('search')
        search_key    = request.GET.get('search_key')
        search_option = {
            0 : Q(title__icontains=search_string) | Q(description__icontains=search_string),
            1 : Q(title__icontains=search_string),
            2 : Q(description__icontains=search_string)
        }   
	
	
        if search_string:
            if not search_key:
                search_key = 0
            query &= search_option[search_key]
       
        boards = Board.objects.select_related('category').filter(query)
	
        if not boards:
            return JsonResponse({'MESSAGE':"PAGE_NOT_FOUND"}, status=404)
        
        total_boards = boards.count()	
        page_count = math.ceil(total_boards/BOARD_COUNT) 

        data = {
            "page" : page,
            "page_count" : page_count,
            "board_count"  : total_boards,
            "boards"    : [{
                "board_id"     : board.id,
                "title"        : board.title,
                "author"       : board.author.nickname,
                "created_at"   : board.created_at,
                "updated_at"   : board.updated_at,
                "views"	: board.views,
            } for board in boards[offset:limit]]}

        return JsonResponse(data,status=200)
  
    @LoginConfirm
    def post(self, request):
        try :
            data      = json.loads(request.body)
            user      = request.user
            Board.objects.create(author=user,title=data["title"],content=data['content']
                ,category=BoardCategory.objects.get(name=data['category']))

            return HttpResponse(status=201)
        
        except KeyError:
            return JsonResponse({"MESSAGE":"KEY_ERROR"}, status = 400)
        
        except json.JSONDecodeError:
            return JsonResponse({"MESSAGE":"INVALID_DATA"}, status=400)
 
class BoardDetailView(View):      
    def get(self, request, board_pk):
        try :
            board = Board.objects.select_related('category').prefetch_related('comment_set').get(id=board_pk)
            board.views += 1
            board.save()
            
            previous_board  = Board.objects.prefetch_related('category').filter(id__lt=board_pk).order_by('id').last()
            next_board      = Board.objects.prefetch_related('category').filter(id__gt=board.pk).order_by('id').first()

            data = {
                "id"         : board.id,
                "author"     : board.author.nickname,
                "title"      : board.title,
                "content"    : board.content,
                "category"   : board.category.name,
                "views"      : board.views,
                "created_at" : board.created_at,
                "updated_at" : board.updated_at,
                "comment"    : [{
                    "id" : comment.id,
                    "author" : comment.author.nickname,
                    "content" : comment.content,
                    "created_at" : comment.created_at,
                    "updated_at" : comment.updated_at
                } for comment in board.comment_set.order_by("-created_at").all()]
            }

            if previous_board:
                data['previous_board'] = {
                    "id"      : previous_board.id,
                    "title"   : previous_board.title,
                    "author"  : previous_board.author.nickname
                }

            if next_board:
                data['next_board'] = {
                    "id"     : next_board.id,
                    "title"  : next_board.title,
                    "author" : next_board.author.nickname
                }
            
            return JsonResponse(data, status=200)

        except Board.DoesNotExist:
            return JsonResponse({'MESSAGE': "BOARD_NOT_FOUND"}, status=404)

        except json.JSONDecodeError:
            return JsonResponse({"MESSAGE": "INVALID_DATA"}, status=400)
    
    @LoginConfirm
    def delete(self, request, board_pk):    
        try:
            board = Board.objects.get(id=board_pk)
            
            if not board.author.id == request.user.id:
                return JsonResponse({"MESSAGE":"UNAUTHORIZED"},status=403)
            
            board.delete()
            return HttpResponse(status=200)

        except Board.DoesNotExist:
            return JsonResponse({"MESSAGE": "BOARD_NOT_FOUND"},status=200)
        
        except json.JSONDecodeError:
            return JsonResponse({"MESSAGE": "INVALID_DATA"},status=400)
    
    @LoginConfirm
    def patch(self, request, board_pk):
        
        try:
            data = json.loads(request.body)
            board = Board.objects.get(id=board_pk)
            
            if not board.author.id == request.user.id:
                return JsonResponse({"MESSAGE":"UNAUTHORIZED"},status=403)

            board.title = data['title']
            board.content = data['content']
            board.save()
        
            return HttpResponse(status=200)
        
        except Board.DoesNotExist:
            return JsonResponse({"MESSAGE":"BOARD_NOT_FOUND"},status=404)
        except KeyError as e:
            return JsonResponse({"MESSAGE":f"KEY_ERROR {e.args[0]}"},status=400)
        except json.JSONDecodeError:
            return JsonResponse({"MESSAGE":"INVALID_DATA"},status=400)
        

class CommentView(View):
    @LoginConfirm
    def post(self, request, board_pk):
        try :
            data      = json.loads(request.body)
            user      = request.user
            Comment.objects.create(author=user,content=data["content"],board=Board.objects.get(id=board_pk))

            return HttpResponse(status=201)
        
        except KeyError:
            return JsonResponse({"MESSAGE":"KEY_ERROR"}, status = 400)
        
        except json.JSONDecodeError:
            return JsonResponse({"MESSAGE":"INVALID_DATA"}, status=400)      

        except Board.DoesNotExist:
            return JsonResponse({'MESSAGE':"BOARD_NOT_FOUND"}, status=404)
    
    @LoginConfirm
    def delete(self, request, board_pk, comment_pk):    
        try:
            comment = Comment.objects.get(board=board_pk,id=comment_pk)
            
            if not comment.author.id == request.user.id:
                return JsonResponse({"MESSAGE":"UNAUTHORIZED"},status=403)
            
            comment.delete()
            return HttpResponse(status=200)

        except Comment.DoesNotExist:
            return JsonResponse({"MESSAGE":"COMMENT_NOT_FOUND"},status=404) 

        except json.JSONDecodeError:
            return JsonResponse({"MESSAGE":"INVALID_DATA"},status=400)
    
    @LoginConfirm
    def patch(self, request, board_pk, comment_pk):
        try:
            data = json.loads(request.body)
            
            comment = Comment.objects.get(id=comment_pk,board=board_pk)
            
            if not comment.author.id == request.user.id:
                return JsonResponse({"MESSAGE":"UNAUTHORIZED"},status=403)
            
            comment.content = data['content']
            comment.save()
        
            return HttpResponse(status=200)
        
        except Comment.DoesNotExist:
            return JsonResponse({"MESSAGE":"COMMENT_NOT_FOUND"},status=404)
        except KeyError as e:
            return JsonResponse({"MESSAGE":f"KEY_ERROR {e.args[0]}"},status=400)
        except json.JSONDecodeError:
            return JsonResponse({"MESSAGE":"INVALID_DATA"},status=400)
        
