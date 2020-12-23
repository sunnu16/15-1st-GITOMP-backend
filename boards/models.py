from django.db    import models
from users.models import User

class BoardCategory(models.Model):
    name = models.CharField(max_length=32)
    
    class Meta:
        db_table = "board_categories"

class Board(models.Model):
    author     = models.ForeignKey(User,on_delete=models.CASCADE)
    title      = models.CharField(max_length=128)
    content    = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    views      = models.IntegerField(default=0)
    category   = models.ForeignKey('BoardCategory',on_delete=models.SET_NULL,null=True)

    class Meta:
        db_table = "boards"

class Comment(models.Model):
    author     = models.ForeignKey(User,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True,null=True)
    board      = models.ForeignKey('Board',on_delete=models.CASCADE)
    content    = models.CharField(max_length=256)
    
    class Meta:
        db_table = "comments"
