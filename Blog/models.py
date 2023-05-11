from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from ckeditor.fields import RichTextField
from django.utils import timezone
import os
from uuid import uuid4

def path_and_rename(instance, filename):
    upload_to = 'media/post_images'
    ext = filename.split('.')[-1]
    # get filename
    if instance.pk:
        filename = '{}.{}'.format(instance.pk, ext)
    else:
        # set filename as random string
        filename = '{}.{}'.format(uuid4().hex, ext)
    # return the whole path to the file
    return os.path.join(upload_to, filename)

CATEGORIES = (
        ('tech', 'Technology'),
        ('food', 'Food'),
        ('travel', 'Travel'),
        ('fashion', 'Fashion'),
        ('sports', 'Sports'),
    )
class Post(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date_published = models.DateTimeField(auto_now_add=True)
    tags = models.CharField(max_length=255)
    category = models.CharField(max_length=255, choices=CATEGORIES)
    image = models.ImageField(upload_to=path_and_rename)
    image_credited = models.CharField(max_length=255, null=True, blank=True)
    body = RichTextField()
    

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])

class Comment(models.Model):
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    date_published = models.DateTimeField(auto_now_add=True)
    reply_comment = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.text
