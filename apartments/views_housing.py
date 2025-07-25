from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Apartment, ApartmentImage, University

@login_required
def add_room(request):
    if request.method == 'POST':
        apartment = Apartment(
            title=request.POST.get('title', 'غرفة للإيجار'),
            description=request.POST.get('description', ''),
            price=request.POST.get('price', 0),
            apartment_type='room',
            area=request.POST.get('area', 20),
            bedrooms=1,
            bathrooms=1,
            address=request.POST.get('address', ''),
            distance_to_university=request.POST.get('distance_to_university', 0),
            university_id=request.POST.get('university'),
            owner=request.user,
            status='pending'
        )
        apartment.save()
        
        for image in request.FILES.getlist('images'):
            ApartmentImage.objects.create(apartment=apartment, image=image)
        
        messages.success(request, 'تم إضافة الغرفة!')
        return redirect('my_apartments')
    
    return render(request, 'apartments/add_room.html', {'universities': University.objects.all()})

@login_required
def add_bed(request):
    if request.method == 'POST':
        apartment = Apartment(
            title=request.POST.get('title', 'سرير للإيجار'),
            description=request.POST.get('description', ''),
            price=request.POST.get('price', 0),
            apartment_type='bed',
            area=request.POST.get('area', 10),
            bedrooms=1,
            bathrooms=1,
            address=request.POST.get('address', ''),
            distance_to_university=request.POST.get('distance_to_university', 0),
            university_id=request.POST.get('university'),
            owner=request.user,
            status='pending'
        )
        apartment.save()
        
        for image in request.FILES.getlist('images'):
            ApartmentImage.objects.create(apartment=apartment, image=image)
        
        messages.success(request, 'تم إضافة السرير!')
        return redirect('my_apartments')
    
    return render(request, 'apartments/add_bed.html', {'universities': University.objects.all()})