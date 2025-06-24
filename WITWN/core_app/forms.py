from django import forms
from .models import Post
from user_app.models import Profile
from .models import Album, Tag
from django.contrib.auth import get_user_model


User = get_user_model()

USERNAME_SYMBOLS = [*list(range(0, 10)), *[chr(num) for num in range(65, 91)], *[chr(num) for num in range(97, 123)], "_"]

class UsernameInput(forms.TextInput):
    def render(self, name, value, attrs = None, renderer = None):
        basic = super().render(name, value, attrs, renderer)
        return f"<div class = 'data-form-username'><p class = 'data-form-sign'>@</p>{basic}</div><p class = 'data-form-hinttext'>Або оберіть: <span class = 'data-form-hint'>Запропоновані варіанти відповідно до Ім’я та Прізвища</span></p>"

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class FirstVisitForm(forms.ModelForm):
    username = forms.CharField(widget = UsernameInput())

    class Meta:
        model = User
        fields = ["first_name", "last_name", "username"]
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["first_name"].widget.attrs.update({"placeholder": "Введіть Ваше ім'я", "required": True})
        self.fields["first_name"].label = "Ім'я"
        self.fields["last_name"].widget.attrs.update({"placeholder": "Введіть Ваше прізвище", "requeired": True})
        self.fields["last_name"].label = "Прізвище"
        self.fields["username"].label = "Ім'я користувача"

    # Who shall we listen to?

    def clean_username(self):
        data: str = self.cleaned_data["username"]
        for symbol in data:
            if symbol not in USERNAME_SYMBOLS:
                raise forms.ValidationError(f'В імені користувача не можна використовувати {symbol}')
            
        return f"@{data}"

# class SettignsInput(forms.TextInput):
#     def __init__(self, attrs = None, shown: bool = False):
#         super().__init__(attrs)
#         self.shown = shown
#     def render(self, name, value, attrs = None, renderer = None):
#         base = super().render(name, value, attrs, renderer)
#         if self.shown:
#             img_source = "{% static 'img/user_base/open_eye.svg' %}"
#         else:
#             img_source = "{% static 'img/user_base/closed_eye.svg' %}"
#         html = f"""<div class = 'settings-input'>{base}<img src = {img_source} class = ""></div>"""
#         return html

class AlbumCreationForm(forms.ModelForm):
    # year = forms.ChoiceField(choices = list(range(1950, 2071)))

    class Meta:
        model = Album
        fields = ["name", "topic"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["name"].label = "Назва альбому"
        self.fields["topic"].label = "Оберіть тему"
        # self.fields["year"].label = "Рік альбому"
        self.fields["name"].widget.attrs.update({"placeholder": "Введіть ім'я"})
        self.fields["topic"].widget.attrs.update({"placeholder": "Оберіть тему"})
        # self.fields["year"].widget.attrs.update({"placeholder": "Оберіть рік"})

class SettingsForm(forms.ModelForm):
    birthday = forms.DateField(required = True)
    # password = forms.CharField(max_length = 200, widget = forms.PasswordInput(render_value = True))
    class Meta:
        model = User
        fields = ["first_name", "last_name", "birthday", "email"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["birthday"].label = "День народженя"
        self.fields["email"].label = "Електронна пошта"
        # Look for password in html, as it is now more complicated
        # self.fields["password"].label = "Пароль"
        # self.fields["password"].widget.attrs.update({"value": "ㅤ"})


class MultipleFileField(forms.FileField):
    def __init__(self, attrs: dict | None = None, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput(attrs = attrs))
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = [single_file_clean(data, initial)]
        return result

# i feel, like im the next one who will fall under his control...

class CreationPostForm(forms.ModelForm):
    topic = forms.CharField(required = True, max_length = 255)
    files = MultipleFileField(required = False, attrs = {'class': "hidden"})
    tags = forms.CharField(required = False, widget = forms.TextInput(attrs = {"class": "hidden"}))
    links = forms.CharField(required = False, widget = forms.TextInput(attrs = {"placeholder": "Додайте посилань до своєї публікації", "class": "creation-input-field"}))
    specific_id = forms.IntegerField(min_value = -1, widget = forms.TextInput(attrs = {"name": "specific_id", "type": "hidden", "value": -1, "class": "hidden"}))
    class Meta:
        model = Post
        fields = ["title", "topic", "content", "links", "tags", "files", "specific_id"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["title"].widget.attrs.update({"placeholder": "Напишіть назву публікації", "class": "creation-input-field"})
        self.fields["topic"].widget.attrs.update({"placeholder": "Напишіть тему публікації", "class": "creation-input-field"})
        self.fields["content"].widget.attrs.update({"placeholder": "Напишіть опис публікації", "class": "creation-input-area"})
        self.fields["links"].widget.attrs.update({"class": "hidden"})
        self.fields["title"].label = "Назва публікації"
        self.fields["topic"].label = "Тема публікації"
        self.fields["content"].label = "Опис публікації"
        self.fields["links"].label = "Посилання"

    def clean_tags(self):
        data = self.cleaned_data["tags"].split(" ")
        if data != "":
            for tag in data.copy():
                if tag != "":
                    if tag[0] != "#":
                        data.remove(tag)
                else:
                    data.remove(tag)
            return data
        else:
            return []

    def clean_files(self):
        return self.files.getlist("files")