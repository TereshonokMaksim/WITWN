from django.shortcuts import redirect
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.auth.views import LogoutView
from django.views.generic.edit import FormView
from django.views.generic.base import TemplateView
from .forms import EmailCodeForm, NewRegForm, NewLoginForm
from django.urls import reverse_lazy
from django.core.mail import EmailMessage
from .models import Profile, VerificationCode, Friendship # no friendship is real under this model structure
from core_app.models import Album, Tag
from django.contrib.auth.hashers import make_password
from django.utils.translation import gettext_lazy
from .utils import email_authenticate
from django.utils import timezone
import random

# Create your views here.

code_symbols = [chr(index) for index in [*range(48, 58)]]

def generate_email_code(length: int = 6):
    return "".join([random.choice(code_symbols) for i in range(length)])

class RegView(FormView):
    template_name = "reg/reg.html"
    form_class = NewRegForm
    success_url = reverse_lazy("reg2")

    def form_valid(self, form: NewRegForm):
        data = form.cleaned_data
        users_with_email = list(User.objects.filter(email = data["email"]))
        if self.request.COOKIES.get("reg_id") != None:
            for user_email in users_with_email.copy():
                if user_email.pk == int(self.request.COOKIES["reg_id"]):
                    users_with_email.remove(user_email)
        
        if len(users_with_email) > 0:
            form.add_error("email", gettext_lazy("This email is already used"))
            return self.form_invalid(form)

        email_code = generate_email_code()
        while len(VerificationCode.objects.filter(code = email_code)) > 0:
            email_code = generate_email_code()
        if self.request.COOKIES.get("reg_id") == None:
            user = User.objects.create_user(username = "none", password = data["password1"], email = data["email"])
            account = Profile(user = user, date_of_birth = timezone.now())
            code = VerificationCode.objects.create(username = user.email, code = email_code)
        else:
            user = User.objects.get(pk = int(self.request.COOKIES["reg_id"]))
            user.email = data["email"]
            user.password = make_password(data["password1"])
            account = Profile.objects.get(user = user)
            VerificationCode.objects.get(username = user.email).code = email_code

        account.save()
        message_text = f"Hello!<br>This is email from WIT Messenger.<br>Enter this code: {email_code} to finish your registration.<br><br>Thanks for choosing us, {user.username}."
        message = EmailMessage("EMail confirmation", message_text, 'danilaageev02@gmail.com', [user.email])
        message.content_subtype = "html"
        message.send()
        response = super().form_valid(form)
        response.set_cookie("reg_id", user.pk, 3600, httponly = True)
        return response
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.COOKIES.get("reg_id") != None:
            acc = User.objects.get(pk = int(self.request.COOKIES["reg_id"]))
            context["email"] = acc.email
        return context

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect('home')
    
class Reg2View(FormView):
    template_name = "reg/confirmation.html"
    form_class = EmailCodeForm
    success_url = reverse_lazy("success")

    def form_valid(self, form):
        data: dict = form.cleaned_data
        code = "".join(str(data[f"symbol{symbol_num}"]) for symbol_num in range(1, 7))
        codes = VerificationCode.objects.filter(code = code)
        if len(codes) == 0:
            return super().form_invalid(form)
        for email_code in codes:
            email_code.code = "0"
            email_code.save()
            break
        
        # Album.objects.create(name = "Мої фото", author = Account.objects.get(user = self.request.user), neccessary = True)
        Album.objects.get_or_create(name = "Мої фото", topic = Tag.objects.first())
        response = super().form_valid(form)
        response.delete_cookie('reg_id')
        return response
    
    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect('home')
    
class ConfirmationView(TemplateView):
    template_name = "reg/reg_success.html"
        
    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect('home')

class LoginView(FormView):
    template_name = 'login/login.html'
    form_class = NewLoginForm
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        data = form.cleaned_data
        account = email_authenticate(email = data["email"], password = data["password"])
        # print(f"Error check: {data}")
        if account:
            login(self.request, account)
            return super().form_valid(form)
        else:
            return super().form_invalid(form)
        
    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect('home')

class CustomLogoutView(LogoutView):
    next_page = reverse_lazy("login")

