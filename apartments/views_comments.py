from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Apartment, Comment, Notification
from .forms import CommentForm, ReplyForm

@login_required
def add_comment(request, apartment_id):
    apartment = get_object_or_404(Apartment, pk=apartment_id)
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.apartment = apartment
            comment.user = request.user
            comment.save()
            messages.success(request, 'تم إضافة التعليق بنجاح')
            return redirect('apartment_detail', pk=apartment_id)
    else:
        form = CommentForm()
    
    return render(request, 'apartments/add_comment.html', {'form': form, 'apartment': apartment})

@login_required
def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    
    if not request.user.is_staff:
        messages.error(request, 'لا يمكنك تعديل التعليقات')
        return redirect('apartment_detail', pk=comment.apartment.id)
    
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            messages.success(request, 'تم تعديل التعليق')
            return redirect('apartment_detail', pk=comment.apartment.id)
    else:
        form = CommentForm(instance=comment)
    
    return render(request, 'apartments/edit_comment.html', {'form': form, 'comment': comment})

@login_required
@require_POST
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    
    if request.user.is_staff:
        apartment_id = comment.apartment.id
        comment.delete()
        messages.success(request, 'تم حذف التعليق')
        return redirect('apartment_detail', pk=apartment_id)
    
    messages.error(request, 'لا يمكنك حذف التعليقات')
    return redirect('apartment_detail', pk=comment.apartment.id)

@login_required
def add_reply(request, comment_id):
    parent_comment = get_object_or_404(Comment, pk=comment_id)
    apartment = parent_comment.apartment
    
    if request.method == 'POST':
        form = ReplyForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.apartment = apartment
            reply.user = request.user
            reply.parent = parent_comment
            reply.save()
            messages.success(request, 'تم إضافة الرد بنجاح')
            return redirect('apartment_detail', pk=apartment.id)
    else:
        form = ReplyForm()
    
    return render(request, 'apartments/add_reply.html', {
        'form': form,
        'parent_comment': parent_comment,
        'apartment': apartment
    })

@login_required
@require_POST
def approve_comment(request, comment_id):
    if request.user.is_staff:
        comment = get_object_or_404(Comment, pk=comment_id)
        comment.is_approved = True
        comment.save()
        messages.success(request, 'تم اعتماد التعليق')
    return redirect('apartment_detail', pk=comment.apartment.id)

@login_required
@require_POST
def reject_comment(request, comment_id):
    if request.user.is_staff:
        comment = get_object_or_404(Comment, pk=comment_id)
        comment.is_approved = False
        comment.save()
        messages.success(request, 'تم رفض التعليق')
    return redirect('apartment_detail', pk=comment.apartment.id)