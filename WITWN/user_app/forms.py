from django import forms
from .models import Account
from django.contrib.auth import authenticate

class RegForm(forms.Form):
    username = forms.CharField(max_length = 256, min_length = 4, widget = forms.TextInput(attrs = {"class": "form-input"}))
    email = forms.EmailField(max_length = 256, min_length = 4, widget = forms.EmailInput(attrs = {"class": "form-input"}))
    password = forms.CharField(max_length = 256, min_length = 4, widget = forms.PasswordInput(attrs = {"class": "form-input"}))
    password_confirm = forms.CharField(max_length = 256, min_length = 4, widget = forms.PasswordInput(attrs = {"class": "form-input"}))

    def clean(self):
        data = self.cleaned_data
        if len(Account.objects.filter(username = data["username"])) > 0:
            raise forms.ValidationError("This username is already taken")
        if len(Account.objects.filter(email = data["email"])) > 0:
            raise forms.ValidationError("This email is already taken")
        if data["password"] != data["password_confirm"]:
            raise forms.ValidationError("Passwords don't match")
        return super().clean()

class LoginForm(forms.Form):
    username = forms.CharField(max_length = 256, min_length = 4, widget = forms.TextInput(attrs = {"class": "form-input"}))
    password = forms.CharField(max_length = 256, min_length = 4, widget = forms.PasswordInput(attrs = {"class": "form-input"}))

    def clean(self):
        data = self.cleaned_data
        user = authenticate(username = data["username"], password = data["password"])
        if user == None:
            print("Incorrect account")
            raise forms.ValidationError('Entered username or password is incorrect')
        if user.email_code != "0":
            print("Incorrect email code")
            raise forms.ValidationError("Confirm your email through the email address that you specified")
        print("dsajdpaosijd")
        return super().clean()

class EmailCodeForm(forms.Form):
    symbol1 = forms.CharField(max_length = 1)
    symbol2 = forms.CharField(max_length = 1)
    symbol3 = forms.CharField(max_length = 1)
    symbol4 = forms.CharField(max_length = 1)
    symbol5 = forms.CharField(max_length = 1)
    symbol6 = forms.CharField(max_length = 1)
