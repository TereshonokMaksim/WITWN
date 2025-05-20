from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from user_app.models import Account
from .models import UserPost, ImageFile
from .forms import CreationPostForm
from django.views import View
from django.urls import reverse_lazy
from django.http import JsonResponse


# Create your views here.

class HomeView(TemplateView):
    template_name = "home/home.html"

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data["posts"] = reversed(list(UserPost.objects.all()))
        if self.request.user.is_authenticated:
            data["account"] = Account.objects.get(user = self.request.user)
        return data

class PublicationsView(FormView):
    template_name = 'my_publications/my_publications.html'
    form_class = CreationPostForm
    success_url = reverse_lazy("my_publications")

    def form_valid(self, form: CreationPostForm):
        data = form.cleaned_data
        print(data["specific_id"], type(data["specific_id"]))
        if data["specific_id"] == -1:
            post = UserPost.objects.create(
                author = Account.objects.get(user = self.request.user),
                title = data['title'],
                theme = data["theme"],
                text = data["text"],
                links = data["links"]
            )
            for file in data["files"]:
                ImageFile.objects.create(file = file, post = post)
        else:
            orig_post = UserPost.objects.get(pk = data["specific_id"])
            if orig_post.author.user == self.request.user:
                print(orig_post.author.user, self.request.user)
                for img in ImageFile.objects.filter(post = orig_post):
                    img.delete()
                orig_post.title = data["title"]
                orig_post.theme = data["theme"]
                orig_post.text = data["text"]
                orig_post.links = data["links"]
                for file in data["files"]:
                    ImageFile.objects.create(file = file, post = orig_post)
                orig_post.save()

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data["form"] = CreationPostForm()
        if self.request.user.is_authenticated:
            data["account"] = Account.objects.get(user = self.request.user)
            data["posts"] = reversed(list(UserPost.objects.filter(author = data["account"])))
        return data

class PostDeleteView(View):
    def get(self, request, *args, **kwargs):
        post = UserPost.objects.filter(pk = kwargs["id"])
        if len(post) != 0:
            post = post[0]
            if post.author.user == request.user:
                post.delete()
        return JsonResponse({"ok": 200})

# class PostCreationView(View):
#     template_name = "my_publications/b.html"
#     # http_method_names = ["GET", "POST"]
#     def post(self, request, *args, **kwargs):
#         form = CreationPostForm(request.POST, request.FILES)
#         if form.is_valid():
#         # print(form.is_valid())

#         # for file in files:

#         return JsonResponse({"OK": 200})