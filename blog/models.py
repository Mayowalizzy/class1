from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Blog(models.Model):
    title = models.CharField(max_length=250)
    category = models.CharField(max_length=50 )
    date = models.DateField(auto_now_add=True)
    context = models.TextField()
    author = models.ForeignKey(User , on_delete = models.CASCADE)
    image = models.ImageField(upload_to="blogs/", default="default.jpg")
    def __str__(self):
        return f"{self.title} by {self.author.username}"

class Comment(models.Model):
    comment= models.TextField()
    date = models.DateField(auto_now_add=True)
    author =  models.ForeignKey(User , on_delete = models.CASCADE)
    likes = models.IntegerField
    blog =  models.ForeignKey(Blog , on_delete = models.CASCADE)
    def __str__(self):
        return f"{self.author.username} commented on {self.blog.title}"
