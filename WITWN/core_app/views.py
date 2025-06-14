from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from user_app.models import Account
from .models import UserPost, ImageFile, Tag, AlbumImageFile, Album, AlbumTheme
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
        acc = Account.objects.get(user = self.request.user)
        data = self.request.POST
        files = self.request.FILES
        return [FirstVisitForm(data, files), CreationPostForm(data, files)][acc.registered]
    
    def form_invalid(self, form: FirstVisitForm):
        print(form.is_bound, "Here")
        return super().form_invalid(form)

    def form_valid(self, form: CreationPostForm | FirstVisitForm):
        data = form.cleaned_data
        print(type(form))
        if isinstance(form, CreationPostForm):
            post_tags = []
            for tag in data["tags"]:
                post_tags.append(Tag.objects.get_or_create(name = tag)[0].pk)
            if data["specific_id"] == -1:
                post = UserPost.objects.create(
                    author = Account.objects.get(user = self.request.user),
                    title = data['title'],
                    theme = data["theme"],
                    text = data["text"],
                    links = data["links"]
                )
                post.tags.set(post_tags)
                for file in data["files"]:
                    ImageFile.objects.create(file = file, post = post)
            else:
                orig_post = UserPost.objects.get(pk = data["specific_id"])
                if orig_post.author.user == self.request.user:
                    # print(orig_post.author.user, self.request.user)
                    for img in ImageFile.objects.filter(post = orig_post):
                        img.delete()
                    orig_post.title = data["title"]
                    orig_post.theme = data["theme"]
                    orig_post.text = data["text"]
                    orig_post.links = data["links"]
                    orig_post.tags.set(post_tags)
                    for file in data["files"]:
                        ImageFile.objects.create(file = file, post = orig_post)
                    orig_post.save()

        elif isinstance(form, FirstVisitForm):
            acc = Account.objects.get(user = self.request.user)
            if not acc.registered:
                acc.user.first_name = data["first_name"]
                acc.user.last_name = data["last_name"]
                acc.user.username = data["username"]
                acc.registered = True
                acc.user.save()
                acc.save()

        else:
            return super().form_invalid(form)

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data["tags"] = Tag.objects.filter(standart = True)
        if self.request.user.is_authenticated:
            data["account"] = Account.objects.get(user = self.request.user)
        return data

class HomeView(PublicationsView):
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data["posts"] = reversed(list(UserPost.objects.all()))
        data["page_name"] = "home"
        data["full_acc"] = True
        return data
    
class MyPublicationsView(PublicationsView):
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            data["posts"] = reversed(list(UserPost.objects.filter(author = data["account"])))
        data["page_name"] = "myPublications"
        data["full_acc"] = False
        return data
        

class PostDeleteView(View):
    def get(self, request, *args, **kwargs):
        post = UserPost.objects.filter(pk = kwargs["id"])
        if len(post) != 0:
            post = post[0]
            if post.author.user == request.user:
                post.delete()
        return JsonResponse({"ok": 200})
    
class FriendsView(TemplateView):
    template_name = 'friends/friends.html'
   
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        acc = Account.objects.get(user = self.request.user)
        data["requests"] = acc.get_requests_accounts()
        if len(data["requests"]) > 6:
            data["requests"] = data["requests"][0:6]
        data["friends"] = acc.get_friends_accounts()
        if len(data["friends"]) > 6:
            data["friends"] = data["friends"][0:6]
        all_possible_recommendations = Account.objects.exclude(pk__in = [acc.pk, *[obj.pk for obj in acc.get_forbidden_accounts()], *[obj.pk for obj in acc.get_requests_accounts()], *[obj.pk for obj in acc.get_friends_accounts()], *[obj.pk for obj in Account.objects.filter(requests__in = [acc.user])]])
        all_possible_recommendations.exclude(registered = False)
        all_possible_recommendations = list(all_possible_recommendations)
        recomendations = []
        for i in range(max(0, min(len(all_possible_recommendations), 5))):
            rec_acc = random.choice(all_possible_recommendations)
            all_possible_recommendations.remove(rec_acc)
            recomendations.append(rec_acc)
        


        data["recomendations"] = recomendations
        data["page_name"] = "friends"
        return data
    
class SettingsView(LoginRequiredMixin, FormView):
    template_name = "settings/settings.html"
    form_class = SettingsForm
    success_url = reverse_lazy("settings")

    def get_initial(self):
        init = super().get_initial()
        user = self.request.user
        acc = Account.objects.get(user = user)
        init["first_name"] = user.first_name
        init["last_name"] = user.last_name
        init["birthday"] = acc.birthday
        init["email"] = user.email
        init["password"] = acc.password
        return init

    def form_valid(self, form: SettingsForm):
        data = form.cleaned_data
        user = self.request.user
        acc = Account.objects.get(user = user)
        acc.birthday = data["birthday"]
        acc.password = data["password"]
        acc.save()
        user.set_password(data["password"])
        update_session_auth_hash(self.request, user)
        user.email = data["email"]
        user.first_name = data["first_name"]
        user.last_name = data["last_name"]
        user.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data["account"] = Account.objects.get(user = self.request.user)
        data["page_name"] = "settings"
        return data

class AlbumsView(ListView):
    template_name = "settings/albums.html"
    context_object_name = "album_list"
    
    def get_queryset(self):
        return Album.objects.filter(author = Account.objects.get(user = self.request.user))

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data["album_themes"] = AlbumTheme.objects.all()
        data["form"] = AlbumCreationForm()
        data["page_name"] = "settings"
        return data

# AJAX endpoints

def check_user(user_checked, user_req, function):
    if user_checked == user_req:
        function()
        return JsonResponse(data = {"request": "success"}, status = 200)
    else:
        return JsonResponse(data = {"request": "permission_denied"}, status = 500)

def delete_album_image(request, *args, **kwargs):
    image = get_object_or_404(AlbumImageFile, pk = kwargs["id"])
    album = image.album
    return check_user(album.author.user, request.user, lambda: image.delete())

def delete_album(request, *args, **kwargs):
    album = get_object_or_404(Album, pk = kwargs["id"])
    if album.necessary:
        print("ERROR!")
        return JsonResponse(data = {"request": "album_necessary"}, status = 500)
    else:
        return check_user(album.author.user, request.user, lambda: album.delete())

def change_visibility(model_obj: AlbumImageFile | Album, visible: int | str):
    model_obj.public = bool(visible)
    model_obj.save()

def change_visibility_image(request, *args, **kwargs):
    image = get_object_or_404(AlbumImageFile, pk = kwargs["id"])
    album = image.album
    return check_user(album.author.user, request.user, lambda: change_visibility(image, kwargs["visibility"]))

def change_visibility_album(request, *args, **kwargs):
    print("What!")
    album = get_object_or_404(Album, pk = int(kwargs["id"]))
    if album.necessary:
        return JsonResponse(data = {"request": "album_necessary"}, status = 500)
    else:
        return check_user(album.author.user, request.user, lambda: change_visibility(album, kwargs["visibility"]))
        

def create_album(request: WSGIRequest, *args, **kwargs):
    if request.method == "POST":
        data = request.POST
        user = request.user
        new_album = Album.objects.create(author = Account.objects.get(user = user), name = data["name"], year = int(data["year"]), theme = AlbumTheme.objects.get(pk = int(data["theme"])))
        return JsonResponse({"request": "success", "id": new_album.pk}, status = 200)
    else:
        return JsonResponse({"request": "incorrect_method"}, status = 500)
    
def add_image(request: WSGIRequest, *args, **kwargs):
    if request.method == "POST":
        data = request.POST

        new_image = AlbumImageFile.objects.create(album = Album.objects.get(pk = data["album_id"]), file = request.FILES["file"])
        return JsonResponse({"request": "success", "id": new_image.pk}, status = 200)
    else:
        return JsonResponse({"request": "incorrect_method"}, status = 500)

# what if we shall look at our creations?

class ChatsView(TemplateView):
    template_name = 'chats/chats.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data["page_name"] = "settings"
        return data
    
def apply_user_changes(request: WSGIRequest, *args, **kwargs):
    user = request.user
    account = Account.objects.get(user = user)
    data = request.POST
    # print(f"LOOK: {data['change_photo'], type(data['change_photo'])}")
    if data["change_photo"] != "false":
        avatar = request.FILES["avatar"]
        account.avatar = avatar
        account.save()
        image_album = Album.objects.filter(author = account).filter(name = "Мої фото").first()
        AlbumImageFile.objects.create(album = image_album, file = avatar)
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

class AllFriendsView(ListView):
    template_name = "friends/friends_list.html"
    context_object_name = "acc_list"
    def get_queryset(self):
        return Account.objects.get(user = self.request.user).get_friends_accounts()
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data["page_name"] = "friends"
        return data
    
class AllRequestsView(ListView):
    template_name = "friends/requests_list.html"
    context_object_name = "acc_list"
    def get_queryset(self):
        return Account.objects.get(user = self.request.user).get_requests_accounts()
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data["page_name"] = "friends"
        return data
    
class AllRecomendationsView(ListView):
    template_name = "friends/recomendations_list.html"
    context_object_name = "acc_list"
    def get_queryset(self):
        acc = Account.objects.get(user = self.request.user)
        all_possible_recommendations = Account.objects.exclude(pk__in = [acc.pk, *[obj.pk for obj in acc.get_forbidden_accounts()], *[obj.pk for obj in acc.get_requests_accounts()], *[obj.pk for obj in acc.get_friends_accounts()], *[obj.pk for obj in Account.objects.filter(requests__in = [acc.user])]])
        all_possible_recommendations.exclude(registered = False)
        all_possible_recommendations = list(all_possible_recommendations)
        recomendations = []
        for i in range(max(0, min(len(all_possible_recommendations), 100))):
            rec_acc = random.choice(all_possible_recommendations)
            all_possible_recommendations.remove(rec_acc)
            recomendations.append(rec_acc)
        return recomendations
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data["page_name"] = "friends"
        return data

def remove_friend(request: WSGIRequest, *args, **kwargs):
    user = request.user
    acc = Account.objects.get(user = user)
    acc.friends.remove(kwargs["id"])
    Account.objects.get(pk = int(kwargs["id"])).friends.remove(acc.pk)
    acc.save()
    return JsonResponse({"request": "sucess"}, status = 200)

def add_friend(request: WSGIRequest, *args, **kwargs):
    user = request.user
    acc = Account.objects.get(user = user)
    acc.requests.remove(kwargs["id"])
    acc.friends.add(kwargs["id"])
    Account.objects.get(pk = int(kwargs["id"])).friends.add(acc.pk)
    acc.save()
    return JsonResponse({"request": "sucess"}, status = 200)

def deny_request(request: WSGIRequest, *args, **kwargs):
    user = request.user
    acc = Account.objects.get(user = user)
    acc.requests.remove(kwargs["id"])
    acc.save()
    return JsonResponse({"request": "sucess"}, status = 200)

def delete_recomendation(request: WSGIRequest, *args, **kwargs):
    user = request.user
    acc = Account.objects.get(user = user)
    acc.forbidden_recommendations.add(kwargs["id"])
    acc.save()
    return JsonResponse({"request": "sucess"}, status = 200)

def send_request(request: WSGIRequest, *args, **kwargs):
    user = request.user
    acc = Account.objects.get(user = user)
    friend_acc = Account.objects.get(pk = int(kwargs["id"]))
    friend_acc.requests.add(acc.pk)
    friend_acc.save()
    return JsonResponse({"request": "sucess"}, status = 200)

class UserView(TemplateView):
    template_name = "friends/user_page.html"

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        user = User.objects.get(pk = self.kwargs["id"])
        acc = Account.objects.get(user = user)
        self_user = self.request.user
        self_acc = Account.objects.get(user = self_user)
        data["account"] = acc
        data["posts"] = UserPost.objects.filter(author = data["account"])
        data["page_name"] = "friends"
        rel = "none"
        if acc.requests.contains(self_user):
            rel = "requested"
        elif self_acc.requests.contains(user):
            rel = "request"
        elif self_acc.friends.contains(user):
            rel = "friends"
        data["relation"] = rel
        return data