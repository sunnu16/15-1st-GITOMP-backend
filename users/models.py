from django.db import models

class User(models.Model):
    nickname = models.CharField(max_length = 16)
    email    = models.EmailField()
    password = models.CharField(max_length = 256)

    class Meta:
        db_table = "users"
