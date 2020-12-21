import json
import math

from django.http      import JsonResponse, HttpResponse
from django.views     import View
from django.db.models import Q

from albums.models    import (Album, Genre, Artist, ReleaseType,
                              PlayLink, AlbumPlayLink)

class AlbumListView(View): 
    def get(self,request):
        
        query       = Q()
        filter_set  = {}
        page        = int(request.GET.get('page',1))
        ALBUM_COUNT = 10
        limit       = ALBUM_COUNT*page
        offset      = limit-ALBUM_COUNT

        if request.GET.get('genre'):
            filter_set['genre__name'] = request.GET['genre']
        
        if request.GET.get('year'):
            filter_set['release_date__year'] = int(request.GET['year'])  

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
            
        
        albums = Album.objects.select_related('genre','release_type').prefetch_related('artist').filter(query,**filter_set)
        
        if not albums:
            return JsonResponse({'MESSAGE':"PAGE_NOT_FOUND"}, status=404)
        
        page_count = math.ceil(albums.count()/ALBUM_COUNT)  
        
        data = {
            "page" : page,
            "page_count" : page_count,
            "albums": [{
                "album_id"     : album.id,
                "title"        : album.title,
                "artist"       : [ artist.name for artist in album.artist.all()],
                "release_type" : album.release_type.name,
                "release_date" : album.release_date,
                "image_url"    : album.image_url
                
            } for album in albums[offset:limit]]}   
        
        return JsonResponse(data,status=200)
        
class AlbumDetailView(View):
    def get(self,request,album_pk):
        try:
            album = Album.objects.select_related(
                'genre','release_type').prefetch_related(
                'artist','song','play_link','albumplaylink_set').get(id=album_pk)
            
            playlinks = album.play_link.prefetch_related("albumplaylink_set","albumplaylink_set_album")

            previous_album  = Album.objects.prefetch_related('artist').filter(id__lt=album_pk).order_by('id').last()
            next_album      = Album.objects.prefetch_related('artist').filter(id__gt=album_pk).order_by('id').first()
            data = {
                "id"                 : album.id,
                "title"              : album.title,
                "artist"             : [artist.name for artist in album.artist.all()],
                "image_url"          : album.image_url,
                "description"        : album.description,
                "description_detail" : album.description_detail,
                "release_date"       : album.release_date,
                "release_type"       : album.release_type.name,
                "genre"              : album.genre.name,
                "song"               : [song.name for song in album.song.all()],
                "playlinks"          : {
                    playlink.name : album_playlink.url for (playlink,album_playlink) in zip(album.play_link.all(),album.albumplaylink_set.all())   
                },    
            }

            if previous_album:
                data["previous_album"] = {
                    "id"     : previous_album.id,
                    "title"  : previous_album.title,
                    "artist" : [artist.name for artist in previous_album.artist.all()]
                }

            if next_album:
                data["next_album"] = {           
                    "id"     : next_album.id,
                    "title"  : next_album.title,
                    "artist" : [artist.name for artist in next_album.artist.all()]
                }

            return JsonResponse(data,status=200)
        
        except Album.DoesNotExist:
            return JsonResponse({"MESSAGE":"ALBUM_NOT_FOUND"},status=404)

class AlbumMainView(View):
    def get(self, request):
        ALBUM_COUNT = 4
        genres = Genre.objects.prefetch_related('album_set','album_set__release_type','album_set__artist').all()
        albums = {}

        for genre in genres:
            albums[genre.name] = [{
                "pk"           : album.id,
                "title"        : album.title,
                "artist"       : [artist.name for artist in album.artist.all()],
                "release_date" : album.release_date,
                "release_type" : album.release_type.name,
                "description"  : album.description,
                "image_url"    : album.image_url,
                "cd_image_url" : album.cd_image_url
            } for album in genre.album_set.all()[:ALBUM_COUNT]]

        return JsonResponse(albums, status=200)
