from django.contrib.auth import logout
from django.shortcuts import redirect

def simple_logout(request):
    """وظيفة بسيطة لتسجيل الخروج"""
    logout(request)
    return redirect('/')
