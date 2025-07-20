from django.shortcuts import redirect
from allauth.socialaccount.models import SocialApp

def social_login(request, provider):
    """
    Redirect to the appropriate social login provider
    """
    if provider == 'google':
        return redirect('/accounts/google/login/?process=login')
    elif provider == 'facebook':
        return redirect('/accounts/facebook/login/?process=login')
    else:
        return redirect('login')