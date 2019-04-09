
from django import template

from django_social_share.templatetags import social_share as ss # post_to_facebook

register = template.Library()

register.inclusion_tag('app/ui/post/facebook.html', takes_context = True)(ss.post_to_facebook)
register.inclusion_tag('app/ui/post/twitter.html', takes_context = True)(ss.post_to_twitter)
register.inclusion_tag('app/ui/post/gplus.html', takes_context = True)(ss.post_to_gplus)