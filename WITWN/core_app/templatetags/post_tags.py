from django import template
from ..models import Image, Post, Link, Album, Tag
from user_app.models import Profile, Friendship

register = template.Library()

@register.inclusion_tag(filename = "post_tags/post.html")

def render_post(post: Post):
    links = []
    for link in Link.objects.filter(post = post):
        links.append(link.url)
    images = list(post.images.all())
    watched_by = len(post.views.all())
    liked_by = len(post.likes.all())
    tag_text = ""
    for tag in post.tags.all():
        tag: Tag
        tag_text += f"{tag.name} "
        print(tag_text, tag, "help") 
    return {"post": post, "links": links, "images": images, "watched_by": watched_by, "liked_by": liked_by, "tag_text": tag_text}

@register.inclusion_tag(filename = "post_tags/profile_and_info.html")

def render_profile_short(account: Profile, detailed: bool = True, album_view: bool = False, relation: str = ""):
    friends = []
    for friendship in Friendship.objects.filter(profile1 = Profile.objects.get(user = account.user), accepted = 1):
        if len(friends) < 3:
            friends.append(friendship.profile2)
    for friendship in Friendship.objects.filter(profile2 = Profile.objects.get(user = account.user), accepted = 1):
        if len(friends) < 3:
            friends.append(friendship.profile1)
    requests = []
    for friendship in Friendship.objects.filter(profile1 = Profile.objects.get(user = account.user), accepted = 0):
        if len(requests) < 3:
            requests.append(friendship.profile2)
    post_num = len(Post.objects.filter(author = account))
    # readers_num = len(account.readers.all())
    readers_num = sum([len(post.views.all()) for post in Post.objects.filter(author = account)])
    # albums = {album: album.images.first() for album in Album.objects.filter(author = account)}
    albums = {album: album.images.first() for album in Album.objects.all()}
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

def render_creation_form(form, account: Profile, tags: list):
    return {"form": form, "account": account, "tags": tags}

# Our watcher is looking at our souls...