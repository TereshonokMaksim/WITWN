from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.views import LogoutView, LoginView
from django.views.generic.edit import FormView
from django.views.generic.base import TemplateView
from .forms import EmailCodeForm, NewRegForm, NewLoginForm
from django.urls import reverse_lazy
from django.core.mail import EmailMessage
from .models import Account
from django.http import HttpRequest
from django.contrib.auth.hashers import make_password
from django.utils.translation import gettext_lazy
import random

# Create your views here.

code_symbols = [chr(index) for index in [*range(48, 58)]]

def generate_email_code(length: int = 6):
    return "".join([random.choice(code_symbols) for repeater in range(length)])

class RegView(FormView):
    template_name = "reg.html"
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
        while len(Account.objects.filter(email_code = email_code)) > 0:
            email_code = generate_email_code()
        if self.request.COOKIES.get("reg_id") == None:
            user = User.objects.create_user(username = data["email"], password = data["password1"], email = data["email"])
            account = Account(user = user, email_code = email_code)
        else:
            user = User.objects.get(pk = int(self.request.COOKIES.get("reg_id")))
            user.username = data["email"]
            user.email = data["email"]
            user.password = make_password(data["password1"])
            account = Account.objects.get(user = user)
            account.email_code = email_code

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
            acc = User.objects.get(pk = int(self.request.COOKIES.get("reg_id")))
            context["email"] = acc.email
        return context

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
class Reg2View(FormView):
    template_name = "confirmation.html"
    form_class = EmailCodeForm
    success_url = reverse_lazy("success")

    def form_valid(self, form):
        data: dict = form.cleaned_data
        code = "".join(str(data[f"symbol{symbol_num}"]) for symbol_num in range(1, 7))
        print(code)
        accounts = Account.objects.filter(email_code = code)
        if len(accounts) == 0:
            return super().form_invalid(form)
        for account in accounts:
            account.email_code = "0"
            account.save()
        
        response = super().form_valid(form)
        response.delete_cookie('reg_id')
        return response

# class CustomLogoutView(LogoutView):
#     templa

class ConfirmationView(TemplateView):
    template_name = "reg_success.html"
    # def dispatch(self, request, *args, **kwargs):
    #     return super().dispatch(request, *args, **kwargs)

class LoginView(FormView):
    template_name = 'login.html'
    form_class = NewLoginForm
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        data = form.cleaned_data
        account = User.objects.get(email = data["email"])
        if account:
            login(self.request, account)
            return super().form_valid(form)
        else:
            return super().form_invalid(form)
    
class HomeView(TemplateView):
    template_name = "home.html"

def home_pass(request):
    return render(request, "passer.html")

def success_pass(request):
    return render(request, "passer.html")

def logout_user(request: HttpRequest):
    logout(request)
    return redirect("home")