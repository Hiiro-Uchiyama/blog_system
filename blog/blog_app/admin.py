from __future__ import unicode_literals
from django.contrib import admin
from .models import Post, Tag
from django_summernote.admin import SummernoteModelAdmin

admin.site.register(Tag)

class PostAdmin(SummernoteModelAdmin):
    summernote_fields = '__all__'

admin.site.register(Post, PostAdmin)