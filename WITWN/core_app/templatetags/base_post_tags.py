from django import template
from ..models import AlbumImageFile, Album

register = template.Library()


@register.inclusion_tag(filename = "post_tags/profile_pic.html")
def get_avatar(account, indicator_on: bool = True):
    indicator_state = ["off", "on"][account.user.is_active]
    if indicator_on:
        ind_path = 'img/home_tt/prof_ind_' + indicator_state + '.svg'
    else:
        ind_path = "png"
    return {"img_path": ind_path, "account": account}

@register.filter
def classname(obj: object):
    return obj.__class__.__name__

@register.filter
def images(album: Album):
    return AlbumImageFile.objects.filter(album = album)

# ...and he sees freedom and independence...