from channels.generic.websocket import AsyncWebsocketConsumer
import json
from .forms import MessageForm
from channels.db import database_sync_to_async
from .models import ChatMessage, ChatGroup
import time
from user_app.models import Profile, Avatar
# from PIL import Image
from io import BytesIO
from django.contrib.auth import get_user_model
import base64
from django.core.files.base import ContentFile
from django.core.cache import cache
# я реально не знаю какой вариант будет лучше для реализации онлайна пользователей


User = get_user_model()

class ChatsConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.allowed = True
        self.group_id = str(self.scope['url_route']['kwargs']['group_id'])
        self.personal = int(self.scope['url_route']['kwargs']['personal'])
        self.group: ChatGroup = await self.auto_check_group()
        if self.allowed:
            self.group_id = str(self.group.pk)
            await self.channel_layer.group_add(
                self.group_id, 
                self.channel_name
            )
            await self.accept()

    async def receive(self, text_data):
        message_data = json.loads(text_data)
        user_profile = await self.get_user_profile(self.scope['user'])
        if message_data["request"] == "message":
            saved_message: ChatMessage = await self.save_message(text_data)
            author = await self.get_message_author(saved_message)
            user = await self.get_user(author)
            if saved_message.attached_image:
                image = saved_message.attached_image.url
            else:
                image = "0"
            await self.channel_layer.group_send(
                self.group_id, 
                {
                    "type": "send_message_to_chat",
                    "message": text_data,
                    "sender": f"{user.first_name} {user.last_name}",
                    "datetime": saved_message.sent_at.isoformat(), 
                    "image": image
                }
            )
            receivers = await self.get_group_members(self.group)
            for receiver in [*receivers]:
                data = {"type": "notification", 
                        "request_type": "message", 
                        "message_content": message_data.get("message"), 
                        "time": saved_message.sent_at.isoformat(),
                        "group": self.group}

                receiver_user = await self.get_user(receiver)
                if cache.get(f"chat_status_user_{receiver_user.pk}") != None:
                    await self.channel_layer.send(cache.get(f"chat_status_user_{receiver_user.pk}"), data)
        elif message_data["request"] == "load":
            messages = await self.get_group_messages()
            data = {"message_data": [], "type": "load", "self_admin": await self.check_admin()}
            for message in messages:
                author = await self.get_message_author(message)
                user = await self.get_user(author)
                if author == user_profile:
                    username = " "
                else:
                    username = f"{user.first_name} {user.last_name}"
                # print(f"ISO: {message.sent_at.isoformat()}")
                if message.attached_image:
                    image = message.attached_image.url
                else:
                    image = "0"
                data["message_data"].append({"message": message.content, "datetime": message.sent_at.isoformat(), "sender": username, "image": image})
            data_JSON = json.dumps(data, ensure_ascii = False)
            await self.send(text_data = data_JSON)
        elif message_data["request"] == "delete":
            data_to_send = {"type": "notification", "request_type": "delete_report", "chat": {"id": self.group.pk, "members": await self.get_group_members(self.group), "is_personal_chat": self.group.is_personal_chat}}
            receivers = await self.get_group_members(self.group)
            for receiver in receivers:
                receiver_user = await self.get_user(receiver)
                if cache.get(f"chat_status_user_{receiver_user.pk}") != None:
                    await self.channel_layer.send(cache.get(f"chat_status_user_{receiver_user.pk}"), data_to_send)
            success = await self.delete_self_group()    
        elif message_data["request"] == "quit":
            success = await self.quit_self_group()
            data_to_send = {"type": "quit_report", "success": success}
            cooked_data = json.dumps(data_to_send)
            await self.send(cooked_data)

        
    async def send_message_to_chat(self, event):
        dict_data = json.loads(event["message"])
        # form = MessageForm(dict_data)
        if True:
            text_to_send = {"type": 'chatting',
                            "message": dict_data["message"],
                            "sender": await self.check_sender(event["sender"]),
                            "datetime": event["datetime"],
                            "image": event["image"]}
            text_data = json.dumps(text_to_send, ensure_ascii = False)
            await self.send(text_data = text_data)
        else:
            print("Error, form isnt valid!")

    @database_sync_to_async
    def get_group_admin(self, group: ChatGroup):
        return group.admin

    @database_sync_to_async
    def get_group_members(self, group: ChatGroup):
        return list(group.members.all())

    @database_sync_to_async
    def quit_self_group(self):
        if self.group.is_personal_chat:
            self.group.delete()
            return True
        else:
            profile = Profile.objects.get(user = self.scope["user"])
            if profile != self.group.admin:
                self.group.members.remove(profile)
                self.group.save()
                return True
            else:
                return False

    @database_sync_to_async
    def delete_self_group(self):
        if self.group.is_personal_chat:
            self.group.delete()
            return True
        else:
            profile = Profile.objects.get(user = self.scope["user"])
            if self.group.admin == profile:
                self.group.delete()
                return True
            else:
                return False
        
    @database_sync_to_async
    def get_message_author(self, message):
        return message.author

    @database_sync_to_async
    def get_user_profile(self, user):
        return Profile.objects.get(user = user)
    
    @database_sync_to_async
    def get_user(self, author):
        return author.user
    
    @database_sync_to_async
    def check_sender(self, username):
        user = self.scope["user"]
        if f"{user.first_name} {user.last_name}" == username:
            return " "
        return username

    @database_sync_to_async
    def auto_check_group(self):
        if self.personal:
            # print("Personal chat1", self.group_id)
            ids = [int(id) for id in self.group_id.split("-")]
            # print(ids, "ID")
            group = ChatGroup.objects.filter(is_personal_chat = True, members__in = [ids[0]]).filter(members__in = [ids[1]])
            # group = group.annotate(member_num = Count("members")).filter(member_num = 2)
            if group.first() == None:
                group = ChatGroup.objects.create(is_personal_chat = True, name = "currentlyunnamed", admin = Profile.objects.first())
                group.members.set([Profile.objects.get(pk = int(id)) for id in self.group_id.split("-")])
                return group
            else:
                # print(group.first())
                return group.first()
        else:
            group = ChatGroup.objects.filter(pk = int(self.group_id))
            if group.first() != None:
                if group.first().members.contains(Profile.objects.get(user = self.scope["user"])):
                    return group.first()
                else:
                    self.allowed = False
                    return group.first()
            else:
                self.allowed = False
                return None

    @database_sync_to_async
    def check_admin(self):
        if self.personal:
            return True
        else:
            return self.group.admin == Profile.objects.get(user = self.scope["user"])

    @database_sync_to_async
    def get_group_messages(self):
        return list(ChatMessage.objects.filter(chat_group_id = self.group_id))

    @database_sync_to_async
    def save_message(self, message_data):
        user = self.scope['user']
        message_data: dict = json.loads(message_data)
        # print(message_data)
        if message_data.get("image") != 0:
            decoded_image = base64.b64decode(message_data.get("image"))
            image = ContentFile(decoded_image, f"{int(time.time())}-message.jpg")
        else:
            image = None
        message = ChatMessage.objects.create(
            content = message_data['message'],
            author = Profile.objects.get(user = user),
            chat_group_id = self.group_id,
            attached_image = image
        )
        return message
    
    @database_sync_to_async
    def get_profile_avatar(self, profile: Profile):
        return Avatar.objects.filter(profile = profile, active = True).first()
    
class ChatStatusConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add(
            f"user_{self.scope['user'].pk}", 
            self.channel_name
        )
        cache.set(f"chat_status_user_{self.scope['user'].pk}", self.channel_name)
        await self.accept()
    
    async def receive(self, text_data: str):
        data: dict = json.loads(text_data)
        if data.get("request_type") == "groupCreation":
            avatar = None
            # print(data)
            avatar_to_send = "0"
            if data.get("avatar") != None and data.get("avatar") != "0":
                base64_data = data.get('avatar')
                data_avatar = base64.b64decode(base64_data)
                avatar = ContentFile(data_avatar, f"{int(time.time())}.jpg")
            members = [int(id) for id in data.get("members")]
            self_prof = await self.get_user_profile(self.scope["user"])
            group = await self.create_group(avatar = avatar, name = data.get("name"), members = members, admin = self_prof)
            if data.get("avatar") != None and data.get("avatar") != "0":
                avatar_to_send = group.avatar.url
            # print(f"new group: {group}, !1, members: {members}, data: {data}")
            for user in await self.get_users(members):
                channel_name = cache.get(f"chat_status_user_{user.pk}")
                if channel_name != None:
                    await self.channel_layer.send(
                        channel_name,
                        {
                            "type": "added_to_group",
                            "name": data["name"],
                            "avatar": avatar_to_send,
                            "group_id": group.id
                        }
                    )
            await self.added_to_group(
                {
                    "type": "added_to_group",
                    "name": data["name"],
                    "avatar": avatar_to_send,
                    "group_id": group.id
                }
            )
        elif data.get("request_type") == "groupEdit":
            data_to_send = []
            group = await self.get_group_by_id(data.get("group_id"))
            members = await self.get_group_members(group)
            for member in members:
                user = await self.get_user_from_profile(member)
                avatar = await self.get_profile_avatar(member)
                data_to_send.append({"id": member.pk, "name": f"{user.first_name} {user.last_name}", "avatar": avatar.image.url})
            raw_data = {"request_type": "groupEdit", "members": data_to_send}
            await self.send(json.dumps(raw_data, ensure_ascii=False))
        elif data.get("request_type") == "groupEditing":
            group = await self.get_group_by_id(int(data.get("group_id")))
            admin = await self.get_group_admin(group)
            new_members = [int(id) for id in data.get("members")]
            old_members_list = await self.get_group_members(group)
            group = await self.edit_group(data)
            old_members_list.append(admin)
            print("editing in progress")
            avatar = group.avatar   
            if avatar != None:
                avatar = avatar.url
            else:
                avatar = "0"
            await self.send(json.dumps({"request_type": "group_edited", "name": group.name, "avatar": avatar, "id": group.pk}))
            for old_member in old_members_list:
                if old_member.pk in new_members:
                    user = await self.get_user_from_profile(old_member)
                    new_members.remove(old_member.pk)
                    mem_channel_name = cache.get(f"chat_status_user_{user.pk}")
                    if mem_channel_name != None:
                        await self.channel_layer.send(mem_channel_name, {"type": "group_edited", "event": {"name": group.name, "avatar": avatar, "id": group.pk}})
                    
                else:
                    if old_member != admin:
                        user = await self.get_user_from_profile(old_member)
                        member_channel_name = cache.get(f"chat_status_user_{user.pk}")
                        if member_channel_name != None:
                            await self.channel_layer.send(member_channel_name, {"type": "deleted_from_group", "event": json.dumps({"request_type": "deleted_from_group", "group_id": group.pk})})

            if len(new_members) > 0:
                avatar = group.avatar
                if avatar != None:
                    avatar = avatar.url
                else:
                    avatar = "0"
                for new_member in new_members:
                    new_member_profile = await self.get_profile_by_id(id = new_member)
                    new_member_user = await self.get_user_from_profile(new_member_profile)
                    new_member_channel = cache.get(f"chat_status_user_{new_member_user.pk}")
                    # print(f"ID: {new_member}, channel name: {new_member_channel}, assembled channel name: 'chat_status_user_{new_member_user.pk}'")
                    if new_member_channel != None:
                        await self.channel_layer.send(
                            new_member_channel,
                            {
                                "type": "added_to_group",
                                "name": group.name,
                                "avatar": avatar,
                                "group_id": group.id
                            }
                        )
                

        elif data.get("request_type") == "infoGet":
            print("Status data: ", data)
            if not data["personal"]:
                group = await self.get_group_by_id(data.get("group_id"))
                member_list = await self.get_group_members(group)
                online = 0
                summary = 0
                for member in member_list:
                    summary += 1
                    user = await self.get_user_from_profile(member)
                    if cache.get(f"user_{user.pk}") != None:
                        online += 1
                await self.send(json.dumps({"request_type": "infoPost", "online": online, "summary": summary}))
            else:
                user = await self.get_users([int(data["group_id"])])
                online = False
                if cache.get(f"user_{user[0].pk}"):
                    online = True
                await self.send(json.dumps({"request_type": "infoPost", "online": online}))

    async def deleted_from_group(self, event: str):
        await self.send(event["event"])

    async def added_to_group(self, event: dict):
        await self.send(json.dumps({"request_type": "added_to_group", "name": event["name"], "avatar": event["avatar"], "id": event["group_id"]}))

    async def group_edited(self, event: dict):
        print("sending group edit", event)
        event = event.get("event")
        await self.send(json.dumps({"request_type": "group_edited", "name": event.get('name'), "avatar": event.get("avatar"), "id": event["id"]}))

    async def notification(self, event: dict):
        if event["request_type"] == "message":
            chat_data = {"id": event["group"].pk, "name": "Unnamed", "avatar": "0", "personal": event['group'].is_personal_chat}
            group = event.get("group")
            if group.is_personal_chat:
                profiles = await self.get_group_members(group)
                self_profile = await self.get_user_profile(self.scope["user"])
                if profiles[0] == self_profile:
                    friend_profile = profiles[1]
                else:
                    friend_profile = profiles[0]
                friend_user = await self.get_users([friend_profile.pk])
                friend_user = friend_user[0]
                chat_data["name"] = f"{friend_user.first_name} {friend_user.last_name}"
                avatar = await self.get_profile_avatar(friend_profile)
                if avatar != None:
                    if avatar.image != None:
                        chat_data["avatar"] = avatar.image.url
                chat_data["id"] = friend_profile.pk
            else:
                avatar = group.avatar
                if avatar != None:
                    chat_data["avatar"] = avatar.url
                chat_data["name"] = event["group"].name
            await self.send(json.dumps({"request_type": "message_notification", 
                                        "message_content": event["message_content"], 
                                        "time": event["time"], 
                                        "chat_data": chat_data}))
        if event["request_type"] == "delete_report":
            group = event.get("chat")
            data = {"request_type": "delete_chat", "chat_id": group["id"], "personal": group["is_personal_chat"]}
            if group["is_personal_chat"]:
                profiles = group["members"]
                self_profile = await self.get_user_profile(self.scope["user"])
                if profiles[0] == self_profile:
                    friend_profile = profiles[1]
                else:
                    friend_profile = profiles[0]
                data["chat_id"] = friend_profile.pk
            await self.send(json.dumps(data))

    @database_sync_to_async
    def get_group_admin(self, chat: ChatGroup):
        return chat.admin

    @database_sync_to_async 
    def get_profile_by_id(self, id: int):
        return Profile.objects.get(id = int(id))

    @database_sync_to_async
    def edit_group(self, data: dict):
        group = ChatGroup.objects.get(pk = data["group_id"])
        group.name = data["name"]
        if data.get("avatar") not in ["0", 0, None]:
            image_code = base64.b64decode(data.get("avatar"))
            avatar = ContentFile(image_code, f"{int(time.time())}.jpg")
            group.avatar = avatar
        members = [int(id) for id in data.get("members")]
        members.append(Profile.objects.get(user = self.scope["user"]).pk)
        group.members.set(members)
        group.save()
        return group
    
    @database_sync_to_async
    def get_profile_avatar(self, profile: Profile):
        return Avatar.objects.filter(profile = profile, active = True).first()

    @database_sync_to_async
    def get_group_by_id(self, id: int):
        return ChatGroup.objects.get(pk = id)

    @database_sync_to_async
    def get_group_members(self, group: ChatGroup):
        return list(group.members.all())

    @database_sync_to_async
    def get_users(self, id_list: list):
        return [Profile.objects.get(id = id).user for id in id_list]

    @database_sync_to_async
    def create_group(self, avatar, name: str, members, admin: Profile):
        group = ChatGroup.objects.create(name = name, avatar = avatar, admin = admin)
        members = [Profile.objects.get(id = id) for id in members]
        members.append(Profile.objects.get(user = self.scope["user"]))
        group.members.set(members)
        return group
    
    @database_sync_to_async
    def get_user_from_profile(self, profile: Profile):
        return profile.user
    
    @database_sync_to_async
    def get_user_profile(self, user):
        return Profile.objects.get(user = user)