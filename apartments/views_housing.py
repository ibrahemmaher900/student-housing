from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Apartment, ApartmentImage, University

@login_required
def add_room(request):
    universities = University.objects.all()
    if request.method == 'POST':
        # استخدم نفس منطق add_apartment في views.py
        from .views import add_apartment
        return add_apartment(request)
    return render(request, 'apartments/add_apartment_new.html', {'universities': universities})

@login_required
def add_bed(request):
    universities = University.objects.all()
    if request.method == 'POST':
        # استخدم نفس منطق add_apartment في views.py
        from .views import add_apartment
        return add_apartment(request)
    return render(request, 'apartments/add_apartment_new.html', {'universities': universities})