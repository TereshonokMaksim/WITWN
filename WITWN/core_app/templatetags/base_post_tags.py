from django import template

register = template.Library()


@register.inclusion_tag(filename = "post_tags/profile_pic.html")
def get_avatar(account):
    indicator_state = ["off", "on"][account.user.is_active]
    ind_path = 'img/home_tt/prof_ind_' + indicator_state + '.svg'
    return {"img_path": ind_path, "account": account}