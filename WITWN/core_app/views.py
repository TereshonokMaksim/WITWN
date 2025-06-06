from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from user_app.models import Account
from .models import UserPost, ImageFile, Tag
from .forms import CreationPostForm, FirstVisitForm, SettingsForm
from django.views import View
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.views.generic import ListView
import random
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import update_session_auth_hash

# Create your views here.


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
        data["friends"] = acc.get_friends_accounts()
        all_possible_recommendations = Account.objects.exclude(pk__in = [acc.pk, *[obj.pk for obj in acc.get_forbidden_accounts()], *[obj.pk for obj in acc.get_requests_accounts()], *[obj.pk for obj in acc.get_friends_accounts()]])
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
