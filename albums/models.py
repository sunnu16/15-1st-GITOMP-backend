from django.db import models

class Artist(models.Model):
    name = models.CharField(max_length=64)

    class Meta:
        db_table = "artists"

class Genre(models.Model):
    name = models.CharField(max_length=32)

    class Meta:
        db_table = "genres"

class ReleaseType(models.Model):
    name = models.CharField(max_length=32)

    class Meta:
        db_table = "release_types"

class PlayLink(models.Model):
    name = models.CharField(max_length=16)

    class Meta:
        db_table = "playlinks"

class Song(models.Model):
    name   = models.CharField(max_length=64)
    writer = models.CharField(max_length=32, null=True)

    class Meta:
        db_table = "songs"

class Album(models.Model):
    title              = models.CharField(max_length=128)
    image_url          = models.URLField(max_length=256)
    description        = models.CharField(max_length=256)
    description_detail = models.TextField()
    release_date       = models.DateTimeField()
    genre              = models.ForeignKey(Genre,on_delete=models.SET_NULL,null=True)
    release_type       = models.ForeignKey(ReleaseType,on_delete=models.SET_NULL,null=True)
    artist             = models.ManyToManyField(Artist,db_table="albums_artists")
    play_link          = models.ManyToManyField(PlayLink,through='AlbumsPlayLink',blank=True)
    song               = models.ManyToManyField(Song,db_table="albums_songs")

    class Meta:
        db_table = "albums"

class AlbumsPlayLink(models.Model):
    albums     = models.ForeignKey(Album,on_delete=models.CASCADE, null=True)
    play_links = models.ForeignKey(PlayLink,on_delete=models.CASCADE, null=True)
    url        = models.URLField(max_length=256)

    class Meta:
        db_table = "albums_playlinks"
