from django import forms
from .models import Post, Tag, Comment
from django.forms import ModelForm
from django_summernote.widgets import SummernoteWidget

## Form for submitting a blog post
class PostAddForm(forms.ModelForm):
   ## The Meta class gives the class the ability to define itself.
   ## Send metadata to models to be stored in the database
   class Meta:
      model = Post
      fields = ['title', 'text', 'image', 'tag']
      ## The basic model is taken from models.py, but overridden by the summernote setting.
      ## Make the interface of the form a summernote.
      text = forms.CharField(widget = SummernoteWidget())

## Form for your enquiry
class ContactForm(forms.Form):
   ## Temporarily define the data structure on the form side.
   name = forms.CharField(label='お名前', max_length=50)
   email = forms.EmailField(label='メールアドレス',)
   message = forms.CharField(label='メッセージ', widget=forms.Textarea)
   myself = forms.BooleanField(label='内容を受け取る', required=False)

## A form for commenting on the blog.
class CmtForm(forms.ModelForm):
   class Meta:
      model = Comment
      fields = ['text']