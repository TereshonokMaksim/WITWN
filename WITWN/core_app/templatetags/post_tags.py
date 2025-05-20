from django import template
from ..models import ImageFile, UserPost

register = template.Library()

@register.inclusion_tag(filename = "post_tags/post.html")

def render_post(post: UserPost):
    links = post.links.split(" ")
    images = list(ImageFile.objects.filter(post = post))
    watched_by = len(post.watched_by.all())
    liked_by = len(post.liked_by.all())
    return {"post": post, "links": links, "images": images, "watched_by": watched_by, "liked_by": liked_by}

@register.inclusion_tag(filename = "post_tags/profile_and_info.html")

def render_profile_short(account, detailed: bool = True):
    friends = account.get_friends_accounts()
    requests = account.get_requests_accounts()
    post_num = len(UserPost.objects.filter(author = account))
    readers_num = len(account.readers.all())
    # print(f"FRIENDS INFO: {friends}")
    return {"account": account, "profile_with_additions": detailed, "friends": friends, "requests": requests, "posts_num": post_num, "readers_num": readers_num}