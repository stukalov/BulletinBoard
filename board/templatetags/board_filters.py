from django import template
from board.models import Bulletin

register = template.Library()


@register.simple_tag(takes_context=True)
def can_edit_bulletin(context, bulletin):
    return bulletin.can_edit(context.request.user)

@register.simple_tag(takes_context=True)
def can_replay_bulletin(context, bulletin):
    return bulletin.can_replay(context.request.user)


@register.simple_tag(takes_context=True)
def url_replace(context, **kwargs):
    d = context['request'].GET.copy()
    for k, v in kwargs.items():
        d[k] = v
    return d.urlencode()
