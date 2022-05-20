from __future__ import unicode_literals
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django_summernote.widgets import SummernoteWidget

## A model for managing blog posts
## Ensure that objects are managed in the order in which they were created.
class PostQuerySet(models.QuerySet):

    ## The data is kept up to date and managed.
    def published(self):
        return self.filter(created_at__lte=timezone.now())

## A data structure that supports blog tags.
class Tag(models.Model):
    tag = models.CharField('タグ名', max_length=50) # Tags support up to 50 characters.

    ## Function to be executed in response to a call such as printf.
    def __str__(self):
        return self.tag

## A model for managing blog posts
class Post(models.Model):
    title = models.CharField('タイトル', max_length=50)
    text = models.TextField('本文')
    image = models.ImageField('画像', upload_to='images', blank=True, null=True) # When you post one blog, you need one image.
    created_at = models.DateTimeField('投稿日', default=timezone.now)
    tag = models.ForeignKey(Tag, verbose_name='タグ', on_delete=models.PROTECT) # It is tied to the tag model we created above.
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    like = models.ManyToManyField(User, related_name='like', blank=True) # Variable to store the user who liked the page
    month = models.CharField('月', max_length=10) # Data to describe the month in three English letters
    date = models.CharField('日付', max_length=5) # Numeric data to represent a date with a maximum of two characters
    objects = PostQuerySet.as_manager() # Variable data called objects can be managed by defining a list of articles that have been submitted

    ## Function to be executed in response to a call such as printf.
    def __str__(self):
        return self.title

## A model to support comments on blog posts
class Comment(models.Model):
    text = models.TextField('コメント') # There is no upper limit to the number of sentences.
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments') # It is tied to a blog post.
    user = models.ForeignKey(User, on_delete=models.CASCADE) # It is tied to the user.
    created_at = models.DateTimeField('投稿日', default=timezone.now)

    ## Function to be executed in response to a call such as printf.
    def __str__(self):
        return self.text