from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from user_app.models import Profile, Avatar
from .models import Post, Image, Album, Tag, Link
from .forms import CreationPostForm, FirstVisitForm, SettingsForm, AlbumCreationForm
from django.views import View
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.views.generic import ListView
import random
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import get_object_or_404
from django.core.handlers.wsgi import WSGIRequest
from django.contrib.auth import get_user_model
import json


# Create your views here.

User = get_user_model()

class PublicationsView(FormView):
    template_name = 'publications/publications.html'
    success_url = reverse_lazy("my_publications")

    def get_form(self):
        acc = Profile.objects.get(user = self.request.user)
        data = self.request.POST
        files = self.request.FILES
        return [FirstVisitForm(data, files), CreationPostForm(data, files)][self.request.user.username != None and self.request.user.username != "none"]
    
    def form_invalid(self, form: FirstVisitForm):
        print(form.is_bound, "Here")
        return super().form_invalid(form)

    def form_valid(self, form: CreationPostForm | FirstVisitForm):
        data = form.cleaned_data
        if isinstance(form, CreationPostForm):
            post_tags = []
            print(data["tags"], "HOW")
            for tag in data["tags"]:
                post_tags.append(Tag.objects.get_or_create(name = tag)[0].pk)
            if data["specific_id"] == -1:
                post = Post.objects.create(
                    author = Profile.objects.get(user = self.request.user),
                    title = data['title'],
                    # theme = data["theme"],
                    content = data["content"],
                )
                for link in data["links"].split(" "):
                    Link.objects.create(url = link, post = post)
                post.tags.set(post_tags)
                for file in data["files"]:
                    post.images.add(Image.objects.create(file = file, filename = "unnamed_post_img"))
            else:
                orig_post = Post.objects.get(pk = data["specific_id"])
                if orig_post.author.user == self.request.user:
                    # print(orig_post.author.user, self.request.user)
                    for img in orig_post.images.all():
                        img.delete()
                        orig_post.images.remove(img.pk)
                    orig_post.title = data["title"]
                    # orig_post.theme = data["theme"]
                    orig_post.content = data["content"]
                    # orig_post.links = data["links"]
                    for link in Link.objects.filter(post = orig_post):
                        link.delete()
                    for new_link in data["links"].split(" "):
                        Link.objects.create(url = new_link, post = orig_post)
                    orig_post.tags.set(post_tags)
                    for file in data["files"]:
                        orig_post.images.add(Image.objects.create(file = file, filename = "unnamed_post_img"))
                    orig_post.save()

        elif isinstance(form, FirstVisitForm):
            user = self.request.user
            acc = Profile.objects.get(user = user)
            if user.first_name == None or user.first_name == "":
                user.first_name = data["first_name"]
                user.last_name = data["last_name"]
                user.username = data["username"]
                user.save()
                acc.save()

        else:
            return super().form_invalid(form)

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data["tags"] = Tag.objects.all()
        # if self.request.user.is_authenticated:
        data["account"] = Profile.objects.get(user = self.request.user)
        return data

class HomeView(PublicationsView):
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data["posts"] = reversed(list(Post.objects.all()))
        profile = Profile.objects.get(user = self.request.user)
        for post in Post.objects.all():
            post.views.add(profile)
        data["page_name"] = "home"
        data["full_acc"] = True
        return data
    
class MyPublicationsView(PublicationsView):
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            data["posts"] = reversed(list(Post.objects.filter(author = data["account"])))
            profile = Profile.objects.get(user = self.request.user)
            for post in Post.objects.filter(author = data["account"]):
                post.views.add(profile)
        data["page_name"] = "myPublications"
        data["full_acc"] = False
        return data
        

class PostDeleteView(View):
    def get(self, request, *args, **kwargs):
        post = Post.objects.filter(pk = kwargs["id"])
        if len(post) != 0:
            post = post[0]
            if post.author.user == request.user:
                post.delete()
        return JsonResponse({"ok": 200})
    
class SettingsView(LoginRequiredMixin, FormView):
    template_name = "settings/settings.html"
    form_class = SettingsForm
    success_url = reverse_lazy("settings")

    def get_initial(self):
        init = super().get_initial()
        user = self.request.user
        acc = Profile.objects.get(user = user)
        init["first_name"] = user.first_name
        init["last_name"] = user.last_name
        init["birthday"] = acc.date_of_birth
        init["email"] = user.email
        # init["password"] = acc.password
        return init

    def form_valid(self, form: SettingsForm):
        data = form.cleaned_data
        user = self.request.user
        acc = Profile.objects.get(user = user)
        acc.date_of_birth = data["birthday"]
        # acc.password = data["password"]
        acc.save()
        # user.set_password(data["password"])
        # update_session_auth_hash(self.request, user)
        user.email = data["email"]
        user.first_name = data["first_name"]
        user.last_name = data["last_name"]
        user.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data["account"] = Profile.objects.get(user = self.request.user)
        data["page_name"] = "settings"
        return data

class AlbumsView(ListView):
    template_name = "settings/albums.html"
    context_object_name = "album_list"
    
    def get_queryset(self):
        # TODO: PAGING
        return Album.objects.filter(author = Profile.objects.get(user = self.request.user))

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data["album_themes"] = Tag.objects.all()
        data["form"] = AlbumCreationForm()
        data["page_name"] = "settings"
        data["avatars"] = Avatar.objects.filter(profile = self.request.user.profile)
        return data

# AJAX endpoints

def check_user(user_checked, user_req, function):
    if user_checked == user_req:
        function()
        return JsonResponse(data = {"request": "success"}, status = 200)
    else:
        print("no")
        return JsonResponse(data = {"request": "permission_denied"}, status = 500)

def delete_album_image(request, *args, **kwargs):
    image = get_object_or_404(Image, pk = kwargs["id"])
    return check_user(request.user, request.user, lambda: image.delete())

def delete_album_avatar(request, *args, **kwargs):
    print("no avatar?")
    image = get_object_or_404(Avatar, pk = kwargs["id"])
    def deleting(avatar: Avatar):
        if avatar.active == False:
            avatar.delete()
        else:
            print("Nuh uh")
            return JsonResponse(data = {"request": "permission_denied"}, status = 500)

    return check_user(request.user, request.user, lambda: deleting(image))

def delete_album(request, *args, **kwargs):
    album = get_object_or_404(Album, pk = kwargs["id"])
    return check_user(request.user, request.user, lambda: album.delete())

def change_visibility(model_obj: Image | Album, visible: int | str):
    # model_obj.public = bool(visible)
    model_obj.save()

def change_visibility_image(request, *args, **kwargs):
    image = get_object_or_404(Image, pk = kwargs["id"])
    # album = image.album
    # return check_user(album.author.user, request.user, lambda: change_visibility(image, kwargs["visibility"]))
    return JsonResponse({"request": "waiting_new_db"}, status = "400")

def change_visibility_album(request, *args, **kwargs):
    # print("What!")
    # album = get_object_or_404(Album, pk = int(kwargs["id"]))
    # if album.necessary:
    #     return JsonResponse(data = {"request": "album_necessary"}, status = 500)
    # else:
    #     return check_user(album.author.user, request.user, lambda: change_visibility(album, kwargs["visibility"]))
    return JsonResponse({"request": "waiting_new_db"}, status = "400")


def create_album(request: WSGIRequest, *args, **kwargs):
    if request.method == "POST":
        data = request.POST
        user = request.user
        # new_album = Album.objects.create(author = Profile.objects.get(user = user), name = data["name"], year = int(data["year"]), theme = AlbumTheme.objects.get(pk = int(data["theme"])))
        new_album = Album.objects.create(name = data["name"], topic = Tag.objects.get(pk = int(data["topic"])), author = user.profile)
        return JsonResponse({"request": "success", "id": new_album.pk}, status = 200)
    else:
        return JsonResponse({"request": "incorrect_method"}, status = 500)
    
def add_image(request: WSGIRequest, *args, **kwargs):
    if request.method == "POST":
        data = request.POST
        if data["album_id"] != "-1":
            new_image = Image.objects.create(file = request.FILES["file"], filename = "unnamed")
            Album.objects.get(pk = data["album_id"]).images.add(new_image)
        else:
            new_image = Avatar.objects.create(image = request.FILES["file"], profile = request.user.profile, shown = True, active = False)
        return JsonResponse({"request": "success", "id": new_image.pk}, status = 200)
    else:
        return JsonResponse({"request": "incorrect_method"}, status = 500)

def apply_user_changes(request: WSGIRequest, *args, **kwargs):
    user = request.user
    account = Profile.objects.get(user = user)
    data = request.POST
    # print(f"LOOK: {data['change_photo'], type(data['change_photo'])}")
    if data["change_photo"] != "false":
        avatar = request.FILES["avatar"]
        # account.avatar = avatar
        # account.save()
        # image_album = Album.objects.filter(author = account).filter(name = "Мої фото").first()
        avatar_to_delete = Avatar.objects.filter(profile = account, active = True).first()
        if avatar_to_delete != None:
            avatar_to_delete.active = False
            avatar_to_delete.save()
        Avatar.objects.create(image = avatar, active = True, profile = account)
    if len(data["username"]) > 0:
        if data["username"][0] != "@":
            username = f"@{data['username'].strip()}"
        else:
            username = data['username']
        user.username = username
        user.save()
    else:
        username = user.username
    return JsonResponse({"request": "success", "username": username}, status = 200)

def change_password(request: WSGIRequest, *args, **kwargs):
    # if request.type == "POST":
    user = request.user
    user.set_password(request.POST.get("password"))
    user.save()
    update_session_auth_hash(request, user)
    return JsonResponse({"request": "success"}, status = 200)
    # else:
    #     return JsonResponse({"request": "incorrect_method"}, status = 500)