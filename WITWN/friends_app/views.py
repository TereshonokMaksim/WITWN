from django.views.generic.base import TemplateView
from user_app.models import Profile, Friendship
from core_app.models import Post
from django.http import JsonResponse
from django.views.generic import ListView
import random
from django.core.handlers.wsgi import WSGIRequest
from django.contrib.auth import get_user_model


# Create your views here.

User = get_user_model()

class FriendsView(TemplateView):
    template_name = 'friends/friends.html'
   
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        acc = Profile.objects.get(user = self.request.user)
        data["requests"] = []
        for friendship in Friendship.objects.filter(profile1 = Profile.objects.get(user = self.request.user), accepted = 0):
            data["requests"].append(friendship.profile2)
        if len(data["requests"]) > 6:
            data["requests"] = data["requests"][0:6]

        data["friends"] = []
        
        for friendship in Friendship.objects.filter(profile1 = Profile.objects.get(user = self.request.user), accepted = 1):
            data["friends"].append(friendship.profile2)
        for friendship in Friendship.objects.filter(profile2 = Profile.objects.get(user = self.request.user), accepted = 1):
            data["friends"].append(friendship.profile1)

        if len(data["friends"]) > 6:
            data["friends"] = data["friends"][0:6]
        
        all_possible_recommendations = Profile.objects.exclude(pk__in = [acc.pk, *[obj.profile2.pk for obj in Friendship.objects.filter(profile1 = acc)], *[obj.profile1.pk for obj in Friendship.objects.filter(profile2 = acc)]])
        all_possible_recommendations = list(all_possible_recommendations)
        recomendations = []
        for i in range(max(0, min(len(all_possible_recommendations), 6))):
            rec_acc = random.choice(all_possible_recommendations)
            all_possible_recommendations.remove(rec_acc)
            recomendations.append(rec_acc)

        data["recomendations"] = recomendations
        data["page_name"] = "friends"
        return data

class AllFriendsView(ListView):
    template_name = "friends_filters/friends_list.html"
    context_object_name = "acc_list"
    def get_queryset(self):
        accs = []
        for friendship in Friendship.objects.filter(profile1 = Profile.objects.get(user = self.request.user), accepted = 1):
            accs.append(friendship.profile2)
        for friendship in Friendship.objects.filter(profile2 = Profile.objects.get(user = self.request.user), accepted = 1):
            accs.append(friendship.profile1)
        return accs
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data["page_name"] = "friends"
        return data
    
class AllRequestsView(ListView):
    template_name = "friends_filters/requests_list.html"
    context_object_name = "acc_list"
    def get_queryset(self):
        accs = []
        for friendship in Friendship.objects.filter(profile1 = Profile.objects.get(user = self.request.user), accepted = 0):
            accs.append(friendship.profile2)
        return 
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data["page_name"] = "friends"
        return data
    
class AllRecomendationsView(ListView):
    template_name = "friends_filters/recomendations_list.html"
    context_object_name = "acc_list"
    def get_queryset(self):
        acc = Profile.objects.get(user = self.request.user)
        all_possible_recommendations = Profile.objects.exclude(pk__in = [acc.pk, *[obj.profile2.pk for obj in Friendship.objects.filter(profile1 = acc)], *[obj.profile1.pk for obj in Friendship.objects.filter(profile2 = acc)]])
        all_possible_recommendations = list(all_possible_recommendations)
        recomendations = []
        for i in range(len(all_possible_recommendations)):
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
    acc = Profile.objects.get(user = user)
    friend_acc = Profile.objects.get(pk = int(kwargs["id"]))
    friend = Friendship.objects.filter(profile1 = acc, profile2 = friend_acc, accepted = 1).first()
    if friend != None:
        friend.delete()
    else:
        friend = Friendship.objects.filter(profile1 = friend_acc, profile2 = acc, accepted = 1).first()
        if friend != None:
            friend.delete()
    return JsonResponse({"request": "sucess"}, status = 200)

def add_friend(request: WSGIRequest, *args, **kwargs):
    user = request.user
    acc = Profile.objects.get(user = user)
    friend_acc = Profile.objects.get(pk = int(kwargs["id"]))
    friendship = Friendship.objects.get(profile1 = acc, profile2 = friend_acc, accepted = 0) 
    friendship.accepted = 1
    friendship.save()
    
    return JsonResponse({"request": "sucess"}, status = 200)

def deny_request(request: WSGIRequest, *args, **kwargs):
    user = request.user
    acc = Profile.objects.get(user = user)
    friend_acc = Profile.objects.get(pk = int(kwargs["id"]))
    friendship = Friendship.objects.get(profile1 = acc, profile2 = friend_acc, accepted = 0) 
    friendship.delete()
    return JsonResponse({"request": "sucess"}, status = 200)

def delete_recomendation(request: WSGIRequest, *args, **kwargs):
    # user = request.user
    # acc = Profile.objects.get(user = user)
    # friend_acc = Profile.objects.get(pk = int(kwargs["id"]))
    # friendship = Friendship.objects.get_or_create(profile1 = acc, profile2 = friend_acc) 
    # friendship.accepted = -1
    # friendship.save()
    
    return JsonResponse({"request": "sucess"}, status = 200)

def send_request(request: WSGIRequest, *args, **kwargs):
    user = request.user
    acc = Profile.objects.get(user = user)
    friend_acc = Profile.objects.get(pk = int(kwargs["id"]))
    Friendship.objects.create(profile1 = friend_acc, profile2 = acc, accepted = 0)
    
    return JsonResponse({"request": "sucess"}, status = 200)

class UserView(TemplateView):
    template_name = "friends/user_page.html"

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        print("error", self.kwargs)
        acc = Profile.objects.get(pk = self.kwargs["id"])
        user = acc.user
        self_user = self.request.user
        self_acc = Profile.objects.get(user = self_user)
        data["account"] = acc
        data["posts"] = Post.objects.filter(author = data["account"])
        data["page_name"] = "friends"
        rel = "none"
        friendship = Friendship.objects.filter(profile1 = acc).first()
        self_friendship = Friendship.objects.filter(profile1 = self_acc).first()
        if friendship != None:
            if friendship.accepted == 0:
                rel = "requested"
            elif friendship.accepted == 1:
                rel = "friends"
        if self_friendship != None and rel == "none":
            if self_friendship.accepted == 0:
                rel = "request"
            elif self_friendship.accepted == 1:
                rel = "friends"
        data["relation"] = rel
        return data