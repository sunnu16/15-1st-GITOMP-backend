from django.db import models

class Location(models.Model):

    name = models.CharField(max_length=64)

    class Meta:
        db_table = "locations"

class Host(models.Model):

    name    = models.CharField(max_length=32)
    contact = models.CharField(max_length=16)

    class Meta:
        db_table = "hosts"

class TicketingSite(models.Model):
    
    name = models.CharField(max_length=16)

    class Meta:
        db_table = "ticketing_sites"

class Seat(models.Model):

    name = models.CharField(max_length=16)
    
    class Meta:
        db_table = "seats"

class Concert(models.Model):

    title            = models.CharField(max_length=64)
    date_performance = models.DateTimeField()
    location         = models.ForeignKey(Location,on_delete=models.SET_NULL,null=True)
    post_url         = models.URLField(max_length=256)
    thumbnail_url    = models.URLField(max_length=256)
    info_detail      = models.TextField()
    date_ticketing   = models.DateTimeField()
    host             = models.ManyToManyField('Host',db_table="concerts_hosts")
    ticketing_site   = models.ManyToManyField(TicketingSite,through='ConcertTicketingSite',blank=True)
    seat             = models.ManyToManyField(Seat,through='ConcertSeat')
    
    class Meta:
        db_table = "concerts"

class ConcertTicketingSite(models.Model):
    
    concert = models.ForeignKey(Concert, on_delete=models.CASCADE,null=True)
    ticketing_site = models.ForeignKey(TicketingSite,on_delete=models.CASCADE,null=True)
    url = models.URLField(max_length=126)

    class Meta:
        db_table = "concerts_ticketing_sites"

class ConcertSeat(models.Model):

    concert = models.ForeignKey(Concert,on_delete=models.CASCADE,null=True)
    seat = models.ForeignKey(Seat,on_delete=models.CASCADE,null=True)
    price = models.IntegerField()

    class Meta:
        db_table = "concerts_seats" 




