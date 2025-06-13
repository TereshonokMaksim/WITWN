from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView, UpdateView
from .models import UserPost, ImageFile, Tag, Album, AlbumImage, AlbumImageFile
from .forms import CreationPostForm, AlbumForm
from user_app.forms import UserProfileForm
from user_app.models import Account
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.views.generic import ListView, CreateView, DeleteView

# Create your views here.


class PublicationsView(FormView):
    template_name = 'publications/publications.html'
    form_class = CreationPostForm
    success_url = reverse_lazy("my_publications")

    def form_valid(self, form: CreationPostForm):
        data = form.cleaned_data
        print(data["specific_id"], type(data["specific_id"]))
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

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data["form"] = CreationPostForm()
        if self.request.user.is_authenticated:
            data["account"] = Account.objects.get(user = self.request.user)
        return data

class HomeView(PublicationsView):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')

        account = Account.objects.get(user=request.user)

        if not account.is_profile_complete():
            form = UserProfileForm(initial={
                'username': request.user.username,
                'first_name': account.first_name,
                'last_name': account.last_name,
            })
            return render(request, 'publications/profile_fill.html', {'form': form})

        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        account = Account.objects.get(user=request.user)

        if not account.is_profile_complete():
            form = UserProfileForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                user = request.user
                user.username = data['username']
                user.save()

                account.first_name = data['first_name']
                account.last_name = data['last_name']
                account.save()

                return redirect('home')

            return render(request, 'publications/profile_fill.html', {'form': form})

        return super().post(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data["posts"] = reversed(list(UserPost.objects.all()))
        data["page_name"] = "home"
        data["full_acc"] = True
        return data

class UserProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = "profile_edit.html"
    success_url = reverse_lazy('profile')

    def get_object(self, queryset=None):
        return self.request.user

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
        context = super().get_context_data(**kwargs)
        account = self.request.user.account

        context['requests'] = account.get_requests_accounts()
        context['friends'] = account.get_friends_accounts()

        excluded_users = list(account.friends.all()) + [self.request.user]
        context['recommended_users'] = User.objects.exclude(id__in = [u.id for u in excluded_users])

        return context


class AcceptFriendRequestView(LoginRequiredMixin, View):
    def post(self, request, user_id):
        account = request.user.account
        requester = get_object_or_404(User, id = user_id)
        if requester in account.requests.all():
            account.requests.remove(requester)
            account.friends.add(requester)
            requester.account.friends.add(request.user)
            messages.success(request, f"Запит від {requester.username} прийнято!")
        else:
            messages.error(request, "Запит не знайдено.")
        return redirect('friends')


class DeclineFriendRequestView(LoginRequiredMixin, View):
    def post(self, request, user_id):
        account = request.user.account
        requester = get_object_or_404(User, id = user_id)
        if requester in account.requests.all():
            account.requests.remove(requester)
            messages.success(request, f"Запит від {requester.username} відхилено.")
        else:
            messages.error(request, "Запит не знайдено.")
        return redirect('friends')


class SendFriendRequestView(LoginRequiredMixin, View):
    def post(self, request, user_id):
        to_user = get_object_or_404(User, id=user_id)
        account = request.user.account

        if to_user != request.user and to_user not in account.friends.all() and to_user not in account.requests.all():
            to_user.account.requests.add(request.user)
            messages.success(request, f"Запит на дружбу відправлено {to_user.username}!")
        else:
            messages.error(request, "Не можна відправити запит.")
        return redirect('friends')


class RemoveFriendView(LoginRequiredMixin, View):
    def post(self, request, user_id):
        friend = get_object_or_404(User, id = user_id)
        account = request.user.account

        if friend in account.friends.all():
            account.friends.remove(friend)
            friend.account.friends.remove(request.user)
            messages.success(request, f"{friend.username} видалений з друзів.")
        else:
            messages.error(request, "Цей користувач не ваш друг.")
        return redirect('friends')
    
class AlbumListView(LoginRequiredMixin, ListView):
    model = Album
    template_name = 'albums/album_list.html'
    context_object_name = 'albums'

    def get_queryset(self):
        return Album.objects.filter(user=self.request.user)

class AlbumCreateView(LoginRequiredMixin, View):
    def get(self, request):
        form = AlbumForm()
        return render(request, 'albums/album_create.html', {'form': form})

    def post(self, request):
        form = AlbumForm(request.POST, request.FILES)
        files = request.FILES.getlist('images')  

        if form.is_valid():
            album = form.save(commit=False)
            album.user = request.user
            album.save()

            for f in files:
                AlbumImageFile.objects.create(file = f, album = album)

            return redirect('album_list')

        return render(request, 'albums/album_create.html', {'form': form})

class AlbumDeleteView(LoginRequiredMixin, DeleteView):
    model = Album
    template_name = 'albums/album_confirm_delete.html'
    success_url = reverse_lazy('album_list')

    def get_queryset(self):
        return Album.objects.filter(user=self.request.user)