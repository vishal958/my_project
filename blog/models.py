from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    # redirect after submit post
    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})


class Comment(models.Model):
    author = models.CharField(max_length=60)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)

    def __str__(self):
        return self.body


class Preference(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    value = models.IntegerField()
    date = models.DateTimeField(auto_now=True)


   
    def __str__(self):
        if self.value == 1:
            return str(self.user) + ' Liked   ' + ' : '+ str(self.post)
        else:
            return str(self.user) + ' Disliked' +':'+ str(self.post)
    class Meta:
        unique_together = ("user", "post", "value")
