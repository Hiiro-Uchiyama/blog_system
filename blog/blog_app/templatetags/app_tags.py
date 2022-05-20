from django import template
from django.utils import timezone
from django.db.models import Count
from django.db.models.functions import TruncMonth
from blog_app.models import Post

register = template.Library()
@register.inclusion_tag('blog_app/includes/month_links.html')
def render_month_links():
    return {
        'dates': Post.objects.published().dates('created_at', 'month', order='DESC'),
    }