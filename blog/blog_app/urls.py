from django.urls import path
from . import views

app_name = 'blog_app'

urlpatterns = [
    path('', views.index, name='index'),
    path('blog', views.blog, name='blog'),
    path('blog', views.IndexView, name='blog'),
    path('detail/<int:post_id>/', views.detail, name='detail'),
    path('contact/', views.contact, name='contact'),
    path('contact/done/', views.done, name='done'),
    path('comment/<int:comment_id>/', views.comment_delete, name='comment_delete'),
    path('archive/<int:year>/',
         views.PostYearArchiveIndex.as_view(), name='year'),
    path('archive/<int:year>/<int:month>/',
         views.PostMonthArchiveIndex.as_view(), name='month'),
    path('about', views.about, name='about'),
    path('service', views.service, name='service'),
    path('menu', views.menu, name='menu'),
    path('movie', views.movie, name='movie'),
    path('case', views.case, name='case'),
]