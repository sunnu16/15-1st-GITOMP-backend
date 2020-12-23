import json
import datetime
import math

from django.http    import JsonResponse
from django.views   import View
from django.db.models import Q
from concerts.models import Concert,Location,ConcertSeat,Host,TicketingSite


#메인페이지/upcomming concert
class ConcertUpcommingView(View):
    def get(self, request):

        #현재시간보다 앞만 뽑기
        concerts = Concert.objects.filter(date_performance__gt = datetime.datetime.now())
        
        if not concerts.exists():
            return JsonResponse({"MESSAGE":"NO_UPCOMMING_CONCERTS"},status=404)

        data = {
            "concerts" : [{
            "pk" : concert.id,
            "title" : concert.title,
            "thumbnail_url" :concert.thumbnail_url
        } for concert in concerts]}
  
        return JsonResponse(data, status=200)
        
#콘서트필터링페이지
class ConcertListView(View):
    def get(self, request):
        query = Q()
        filter ={}
        CONCERT_COUNT = 10
        page = int(request.GET.get('page',1))
        limit = CONCERT_COUNT * page
        offset = limit -CONCERT_COUNT

        search_list = Concert.objects.all() 
        search_string = request.GET.get('search')
        search_key = request.GET.get('search_key')

        #year 필터 
        if request.GET.get('year'):
            filter['date_performance__year'] = request.GET['year']

        if request.GET.get('title'):
            filter['title'] = request.GET['title']

        #전체,제목,내용 검색 경우의 수+내용이 없을때
            search_option= {
            
            
            #번호통일수정하기 / search_data ->string으로변경하기
            0 : (Q(info_detail__icontains = search_string) | Q(tilte__icontains = search_string)),
            1 : Q(info_detail__icontains = search_string),
            2 : Q(title__icontains = search_string)
            }

        if search_string:

            if not search_key:

                serarch_key = 0

            query &= search_option[search_key]

        concerts= Concert.objects.select_related('location').prefetch_related('seat', 'host', 'ticketing_site').filter(query, **filter)

        if not concerts:
            return JsonResponse({'message' : "page_not_found"}, status = 404)

        page_count = math.ceil(concerts.count()/CONCERT_COUNT)
        data = {
            "concert" :[{
                "id" : concert.id,
                "title" : concert.title,
                "location" : concert.location.name,
                "date_performance" : concert.date_performance,
                "post_url" : concert.post_url,
                "seats" : [{
                    "name" : seat.name,
                    "price": ConcertSeat.objects.get(concert=concert.id,seat=seat.id)
                } for seat in concert.seat.all()],
                "date_ticketing" : concert.date_ticketing
            }for concert in concerts[offset:limit]]}

        return JsonResponse(data, status = 200)



#상세페이지
class ConcertDetailView(View):
    def get(self, reqeust, concert_id):
        try:
            concert =Concert.objects.select_related('location').prefetch_related('seat','host','ticketing_site').get(id=concert_id)
            #preious로 맞추기
            previous_concert = Concert.objects.filter(id__lt=concert_id).order_by('id').first()
            next_concert = Concert.objects.filter(id__gt=concert_id).order_by('id').first()

            data = {
                'id' : concert.id,
                'title' : concert.title,
                'date_performance' : concert.date_performance,
                'location' :concert.location.name,
                'post_url' : concert.post_url,
                'thumbnail_url' : concert.thumbnail_url,
                'info_detail' : concert.info_detail,

                'host' : [{
                    "name" : host.name,
                    "phone" : host.contact
                } for host in concert.host.all()],

                "seat" : [{
                    "seat" : seat.name,
                    "price" : ConcertSeat.objects.get(concert=concert.id,seat=seat.id).price
                } for seat in concert.seat.all()]
            }
            
            if concert.date_ticketing:
                data['date_ticketing'] = concert.date_ticketing


            #하단 이전,다음글
            if previous_concert :
                data['previous_concert'] = {
                    "id" : previous_concert.id,
                    "title" :previous_concert.title      
                }
            if next_concert : 
                data['next_concert'] = {
                    "id" : next_concert.id,
                    "title" : next_concert.title
                }
            
            return JsonResponse(data , status=200)

        except Concert.DoesNotExist:
            return JsonResponse({"message":"concert not found"}, status=404)


