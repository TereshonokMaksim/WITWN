from django.shortcuts import render
from django.views.generic.list import ListView
# from user_app.models import Account
from django.views.generic.base import TemplateView
from .models import ChatGroup, ChatMessage
from user_app.models import Profile, Friendship


# Create your views here.

class ChatsView(TemplateView):
    template_name = 'chats/chats.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['friends'] = []
        for friendship in Friendship.objects.filter(profile1 = Profile.objects.get(user = self.request.user), accepted = 1):
            data["friends"].append(friendship.profile2)
        for friendship in Friendship.objects.filter(profile2 = Profile.objects.get(user = self.request.user), accepted = 1):
            data["friends"].append(friendship.profile1)
        data["page_name"] = "chats"
        data["groups"] = {}
        groups = ChatGroup.objects.filter(is_personal_chat = False, members__in = [Profile.objects.get(user = self.request.user)])
        for group in groups:
            data["groups"].update({group: ChatMessage.objects.filter(chat_group = group).last()})
        data["messages"] = {}
        self_profile = Profile.objects.get(user = self.request.user)
        messages = ChatGroup.objects.filter(is_personal_chat = True, members__in = [Profile.objects.get(user = self.request.user)])
        for message in messages:
            print("More: ", message.members.all())
            message_ = ChatMessage.objects.filter(chat_group = message).last()
            print("Message: ", message_)
            if message_ != None:
                profile = None
                if message.members.first() == self_profile:
                    profile = message.members.all()[1]
                else:
                    profile = message.members.first()
                data["messages"].update({profile: message_})

        return data