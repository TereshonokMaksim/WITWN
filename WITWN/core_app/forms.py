from django import forms
from .models import UserPost


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

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

class CreationPostForm(forms.ModelForm):
    files = MultipleFileField(required = False, attrs = {'class': "hidden"})
    tags = forms.CharField(required = False, widget = forms.TextInput(attrs = {"class": "hidden"}))
    links = forms.CharField(required = False, widget = forms.TextInput(attrs = {"placeholder": "Додайте посилань до своєї публікації", "class": "creation-input-field"}))
    specific_id = forms.IntegerField(min_value = -1, widget = forms.TextInput(attrs = {"name": "specific_id", "type": "hidden", "value": -1, "class": "hidden"}))
    class Meta:
        model = UserPost
        fields = ["title", "theme", "text", "links", "tags", "files", "specific_id"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["title"].widget.attrs.update({"placeholder": "Напишіть назву публікації", "class": "creation-input-field"})
        self.fields["theme"].widget.attrs.update({"placeholder": "Напишіть тему публікації", "class": "creation-input-field"})
        self.fields["text"].widget.attrs.update({"placeholder": "Напишіть опис публікації", "class": "creation-input-area"})
        self.fields["links"].widget.attrs.update({"class": "hidden"})
        self.fields["title"].label = "Назва публікації"
        self.fields["theme"].label = "Тема публікації"
        self.fields["text"].label = "Опис публікації"
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