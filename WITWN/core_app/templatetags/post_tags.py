from django import template
from ..models import ImageFile, UserPost, Album, AlbumImageFile
from user_app.models import Account

register = template.Library()

@register.inclusion_tag(filename = "post_tags/post.html")

def render_post(post: UserPost):
    links = post.links.split(" ")
    images = list(ImageFile.objects.filter(post = post))
    watched_by = len(post.watched_by.all())
    liked_by = len(post.liked_by.all())
    tag_text = ""
    for tag in post.tags.all():
        tag_text += f"{tag.name} "
    return {"post": post, "links": links, "images": images, "watched_by": watched_by, "liked_by": liked_by, "tag_text": tag_text}

@register.inclusion_tag(filename = "post_tags/profile_and_info.html")

def render_profile_short(account: Account, detailed: bool = True, album_view: bool = False, relation: str = ""):
    friends = account.get_friends_accounts()
    requests = account.get_requests_accounts()
    post_num = len(UserPost.objects.filter(author = account))
    readers_num = len(account.readers.all())
    albums = {album: AlbumImageFile.objects.filter(album = album).first() for album in Album.objects.filter(author = account)}
    return {"account": account, 
            "profile_with_additions": detailed, 
            "friends": friends, 
            "requests": requests, 
            "posts_num": post_num, 
            "readers_num": readers_num,
            "albums_need": album_view,
            "albums": albums,
            "relation": relation}

@register.inclusion_tag(filename = "post_tags/create_post_form.html")

def render_creation_form(form, account: Account, tags: list):
    return {"form": form, "account": account, "tags": tags}

# Our watcher is looking at our souls...