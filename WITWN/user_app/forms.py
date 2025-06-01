from django import forms
from .models import Account
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.utils.translation import gettext_lazy
from django.core.validators import EmailValidator

email_validator = EmailValidator()

class NewLoginForm(AuthenticationForm):
    # Костылиии
    username = forms.EmailField(
        label=gettext_lazy("Електронна пошта"),
        widget=forms.EmailInput(attrs={'autofocus': True, 'autocomplete': 'email'})
    )

    def __init__(self, request = ..., *args, **kwargs):
        super().__init__(request, *args, **kwargs)
        self.user_cache: User

    def clean(self):
        data = self.cleaned_data
        print(data)
        data["email"] = data["username"]
        user = authenticate(username = data["email"], password = data["password"])
        if user == None:
            raise forms.ValidationError(gettext_lazy("Incorrect password or email"))
        else:
            account = Account.objects.get(user = user)
            if account.email_code == "0":
                self.user_cache = user
                return data
            else:
                raise forms.ValidationError(gettext_lazy("Complete your email confirmation first"))
            
    def clean_username(self):
        print('as')
        data = self.cleaned_data["username"]
        return data
            
    def get_user(self) -> User:
        return self.user_cache

class NewRegForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("email", "password1", "password2")

# class RegForm(forms.Form):
#     username = forms.CharField(max_length = 256, min_length = 4, widget = forms.TextInput(attrs = {"class": "form-input"}))
#     email = forms.EmailField(max_length = 256, min_length = 4, widget = forms.EmailInput(attrs = {"class": "form-input"}))
#     password = forms.CharField(max_length = 256, min_length = 4, widget = forms.PasswordInput(attrs = {"class": "form-input"}))
#     password_confirm = forms.CharField(max_length = 256, min_length = 4, widget = forms.PasswordInput(attrs = {"class": "form-input"}))

#     def clean(self):
#         data = self.cleaned_data
#         if len(Account.objects.filter(username = data["username"])) > 0:
#             raise forms.ValidationError("This username is already taken")
#         if len(Account.objects.filter(email = data["email"])) > 0:
#             raise forms.ValidationError("This email is already taken")
#         if data["password"] != data["password_confirm"]:
#             raise forms.ValidationError("Passwords don't match")
#         return super().clean()

# class LoginForm(forms.Form):
#     username = forms.CharField(max_length = 256, min_length = 4, widget = forms.TextInput(attrs = {"class": "form-input"}))
#     password = forms.CharField(max_length = 256, min_length = 4, widget = forms.PasswordInput(attrs = {"class": "form-input"}))

#     def clean(self):
#         data = self.cleaned_data
#         user = authenticate(username = data["username"], password = data["password"])
#         if user == None:
#             print("Incorrect account")
#             raise forms.ValidationError('Entered username or password is incorrect')
#         if user.email_code != "0":
#             print("Incorrect email code")
#             raise forms.ValidationError("Confirm your email through the email address that you specified")
#         print("dsajdpaosijd")
#         return super().clean()

class EmailCodeForm(forms.Form):
    symbol1 = forms.CharField(max_length = 1)
    symbol2 = forms.CharField(max_length = 1)
    symbol3 = forms.CharField(max_length = 1)
    symbol4 = forms.CharField(max_length = 1)
    symbol5 = forms.CharField(max_length = 1)
    symbol6 = forms.CharField(max_length = 1)
