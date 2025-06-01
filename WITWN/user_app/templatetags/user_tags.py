from django import template
import os

register = template.Library()

@register.inclusion_tag(filename = os.path.join("user_base", "form_base_tag.html"))
def user_form(form, button_submit_text: str):
    return {"form": form, "button_submit_text": button_submit_text}