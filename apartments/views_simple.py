from django.shortcuts import render

def simple_home(request):
    """صفحة رئيسية بسيطة لا تستخدم مسار 'profile'"""
    return render(request, 'apartments/simple_home.html')
