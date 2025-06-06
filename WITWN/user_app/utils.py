from django.contrib.auth import get_user_model


User = get_user_model()

def email_authenticate(email: str, password: str):
    '''
        Same as usual authenticate funciton, but with email.
        Made because username is taken by user's data.
    '''
    user = User.objects.filter(email = email)
    if user.exists():
        if user[0].check_password(password):
            return user[0]
    return None 