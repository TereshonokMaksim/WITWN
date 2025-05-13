from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.views import LogoutView, LoginView
from django.views.generic.edit import FormView
from django.views.generic.base import TemplateView
from .forms import LoginForm, RegForm, EmailCodeForm
from django.urls import reverse_lazy
from django.core.mail import EmailMessage
from .models import Account
from django.http import HttpRequest
from django.contrib.auth.hashers import make_password
import random

# Create your views here.

code_symbols = [chr(index) for index in [*range(48, 58)]]

def generate_email_code(length: int = 6):
    return "".join([random.choice(code_symbols) for repeater in range(length)])

class RegView(FormView):
    template_name = "reg.html"
    form_class = RegForm
    success_url = reverse_lazy("reg2")

    def form_valid(self, form):
        data = form.cleaned_data
        email_code = generate_email_code()
        while len(Account.objects.filter(email_code = email_code)) > 0:
            email_code = generate_email_code()
        if self.request.COOKIES.get("reg_id") == None:
            account = Account.objects.create_user(username = data["username"], password = data["password"], email = data["email"], email_code = email_code)
        else:
            account = Account.objects.get(pk = int(self.request.COOKIES.get("reg_id")))
            account.username = data["username"]
            account.email = data["email"]
            account.password = make_password(data["password"])
            account.email_code = email_code
        message_text = f"Hello!<br>This is email from WIT Messenger.<br>Enter this code: {email_code} to finish your registration.<br><br>Thanks for choosing us, {account.username}."
        message = EmailMessage("EMail confirmation", message_text, 'danilaageev02@gmail.com', [account.email])
        message.content_subtype = "html"
        message.send()
        response = super().form_valid(form)
        response.set_cookie("reg_id", account.pk, 3600, httponly = True)
        return response
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.COOKIES.get("reg_id") != None:
            acc = Account.objects.get(pk = int(self.request.COOKIES.get("reg_id")))
            context["username"] = acc.username
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
    form_class = LoginForm
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        data = form.cleaned_data
        account = Account.objects.get(username = data["username"])
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