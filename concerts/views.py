import json
import datetime
import math

from django.http         import JsonResponse
from django.views        import View
from django.db.models    import Q

from concerts.models     import Concert,Location,ConcertSeat,Host,TicketingSite

class ConcertUpcommingView(View):
    def get(self, request):
        concerts = Concert.objects.filter(date_performance__gt = datetime.datetime.now()).order_by('date_performance')
        
        if not concerts.exists():
            return JsonResponse({"MESSAGE":"NO_UPCOMMING_CONCERTS"},status=404)

        data = {
                "concerts"          : [{
                    "pk"                : concert.id,
                    "title"             : concert.title,
                    "thumbnail_url"     : concert.thumbnail_url
            } for concert in concerts]}
        return JsonResponse(data, status=200)
        
class ConcertListView(View):
    def get(self, request):
        
        query         = Q()
        CONCERT_COUNT = 10
        page          = int(request.GET.get('page',1))
        limit         = CONCERT_COUNT * page
        offset        = limit - CONCERT_COUNT
        
        search_list   = Concert.objects.all()

        year          = request.GET.get('year')
        search_string = request.GET.get('search')
        search_key    = request.GET.get('search_key',0)

        if year:
            query = Q(date_performance__year = int(year)) 
        
        if search_string:
            search_option= {                   
                0 : Q(info_detail__icontains = search_string) | Q(title__icontains = search_string),
                1 : Q(title__icontains = search_string),
                2 : Q(info_detail__icontains = search_string)
            }

            query &= search_option[int(search_key)]
    

        concerts = Concert.objects.select_related('location').prefetch_related('seat', 'host', 'ticketing_site').filter(query).order_by('-date_performance')
        
        if not concerts:
            return JsonResponse({'message' : "PAGE_NOT_FOUND"}, status = 404)

        page_count = math.ceil(concerts.count() / CONCERT_COUNT)
        
        data = {
            "page"                 : page,
            "page_count"           : page_count,
            "concert"              : [{
                "id"               : concert.id,
                "title"            : concert.title,
                "location"         : concert.location.name,
                "date_performance" : concert.date_performance.date(),
                "post_url"         : concert.post_url,
                "seats"            : [{
                    "name"      : seat.name,
                    "price"     : ConcertSeat.objects.get(concert=concert.id,seat=seat.id).price
                } for seat in concert.seat.all()],
                "date_ticketing" : concert.date_ticketing
            }for concert in concerts[offset:limit]]}

        return JsonResponse(data, status = 200)

class ConcertDetailView(View):
    def get(self, reqeust, concert_id):
        try:
            concert          = Concert.objects.select_related('location').prefetch_related('seat','host','ticketing_site').get(id=concert_id)         
            previous_concert = Concert.objects.filter(date_performance__lt=concert.date_performance).order_by('date_performance').last()
            next_concert     = Concert.objects.filter(date_performance__gt=concert.date_performance).order_by('date_performance').first()
            
            data = {
                'id'               : concert.id,
                'title'            : concert.title,
                'date_performance' : concert.date_performance.date(),
                'location'         : concert.location.name,
                'post_url'         : concert.post_url,
                'thumbnail_url'    : concert.thumbnail_url,
                'info_detail'      : concert.info_detail,
                'host'             : [{
                    "name"  : host.name,
                    "phone" : host.contact
                } for host in concert.host.all()],
                "seat" : [{
                    "seat"  : seat.name,
                    "price" : ConcertSeat.objects.get(concert=concert.id,seat=seat.id).price
                } for seat in concert.seat.all()]
            }
            
            if concert.date_ticketing:
                data['date_ticketing'] = concert.date_ticketing.date()

            if previous_concert :
                data['previous_concert'] = {
                    "id" : previous_concert.id,
                    "title" :previous_concert.title      
                }
            if next_concert : 
                data['next_concert'] = {
                    "id"    : next_concert.id,
                    "title" : next_concert.title
                }
            return JsonResponse(data,status=200)

        except Concert.DoesNotExist:
            return JsonResponse({"MESSAGE":"CONCERT_NOT_FOUND"}, status=404)


