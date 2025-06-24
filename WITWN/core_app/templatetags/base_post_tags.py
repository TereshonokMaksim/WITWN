from django import template
from ..models import Image, Album
from user_app.models import Avatar, Profile
from django.core.cache import cache

register = template.Library()


@register.inclusion_tag(filename = "post_tags/profile_pic.html")
def get_avatar(account: Profile, indicator_on: bool = True):
    indicator_state = ["off", "on"][cache.get(f"user_{account.user.pk}") != None]
    print("Account: ", account.user.first_name, "indicator state: ", indicator_state)
    if indicator_on:
        ind_path = 'img/home_tt/prof_ind_' + indicator_state + '.svg'
    else:
        ind_path = "png"
    avatar = Avatar.objects.filter(profile = account, active = True).first()
    if avatar == None:
        avatar = "none"
    return {"img_path": ind_path, "avatar": avatar}

@register.filter
def classname(obj: object):
    return obj.__class__.__name__

@register.filter
def images(album: Album):
    return album.images.all()

@register.filter
def all_but_first(text: str):
    return text[1:]

# ...and he sees freedom and independence...