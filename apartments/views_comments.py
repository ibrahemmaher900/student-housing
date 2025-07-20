from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Apartment, Comment, Notification
from .forms import CommentForm, ReplyForm

@login_required
def add_comment(request, apartment_id):
    """إضافة تعليق جديد على شقة"""
    apartment = get_object_or_404(Apartment, pk=apartment_id)
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.apartment = apartment
            comment.user = request.user
            comment.save()
            
            # إنشاء إشعار لمالك الشقة
            if request.user != apartment.owner:
                Notification.objects.create(
                    user=apartment.owner,
                    notification_type='new_comment',
                    message=f'قام {request.user.username} بإضافة تعليق على شقتك {apartment.title}',
                    related_apartment=apartment,
                    related_comment=comment
                )
            
            # التحقق من نوع الطلب (AJAX أو عادي)
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'status': 'success',
                    'message': 'تم إضافة تعليقك بنجاح'
                })
            else:
                messages.success(request, 'تم إضافة تعليقك بنجاح')
                return redirect('apartment_detail', pk=apartment_id)
        else:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'status': 'error',
                    'message': 'حدث خطأ في النموذج'
                })
    else:
        form = CommentForm()
    
    context = {
        'form': form,
        'apartment': apartment
    }
    return render(request, 'apartments/add_comment.html', context)

@login_required
def edit_comment(request, comment_id):
    """تعديل تعليق (للمسؤولين فقط)"""
    comment = get_object_or_404(Comment, pk=comment_id)
    
    # التحقق من أن المستخدم هو مسؤول
    if not request.user.is_staff:
        messages.error(request, 'لا يمكنك تعديل التعليقات. هذه الصلاحية متاحة للمسؤولين فقط')
        return redirect('apartment_detail', pk=comment.apartment.id)
    
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            messages.success(request, 'تم تعديل التعليق بنجاح')
            return redirect('apartment_detail', pk=comment.apartment.id)
    else:
        form = CommentForm(instance=comment)
    
    context = {
        'form': form,
        'comment': comment
    }
    return render(request, 'apartments/edit_comment.html', context)

@login_required
@require_POST
def delete_comment(request, comment_id):
    """حذف تعليق (للمسؤولين فقط)"""
    comment = get_object_or_404(Comment, pk=comment_id)
    
    # التحقق من أن المستخدم هو مسؤول
    if not request.user.is_staff:
        messages.error(request, 'لا يمكنك حذف التعليقات. هذه الصلاحية متاحة للمسؤولين فقط')
        return redirect('apartment_detail', pk=comment.apartment.id)
    
    apartment_id = comment.apartment.id
    comment.delete()
    messages.success(request, 'تم حذف التعليق بنجاح')
    return redirect('apartment_detail', pk=apartment_id)

@login_required
def add_reply(request, comment_id):
    """إضافة رد على تعليق"""
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
            
            # إنشاء إشعار لصاحب التعليق الأصلي
            if request.user != parent_comment.user:
                Notification.objects.create(
                    user=parent_comment.user,
                    notification_type='comment_reply',
                    message=f'قام {request.user.username} بالرد على تعليقك على شقة {apartment.title}',
                    related_apartment=apartment,
                    related_comment=reply
                )
            
            messages.success(request, 'تم إضافة ردك بنجاح')
            return redirect('apartment_detail', pk=apartment.id)
    else:
        form = ReplyForm()
    
    context = {
        'form': form,
        'parent_comment': parent_comment,
        'apartment': apartment
    }
    return render(request, 'apartments/add_reply.html', context)

@login_required
@require_POST
def approve_comment(request, comment_id):
    """اعتماد تعليق (للمسؤولين فقط)"""
    comment = get_object_or_404(Comment, pk=comment_id)
    
    # التحقق من أن المستخدم هو مسؤول
    if not request.user.is_staff:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'status': 'error',
                'message': 'ليس لديك صلاحية اعتماد التعليقات. هذه الصلاحية متاحة للمسؤولين فقط'
            })
        else:
            messages.error(request, 'ليس لديك صلاحية اعتماد التعليقات. هذه الصلاحية متاحة للمسؤولين فقط')
            return redirect('apartment_detail', pk=comment.apartment.id)
    
    comment.is_approved = True
    comment.save()
    
    # إنشاء إشعار لصاحب التعليق
    if request.user != comment.user:
        Notification.objects.create(
            user=comment.user,
            notification_type='new_comment',
            message=f'تمت الموافقة على تعليقك على شقة {comment.apartment.title}',
            related_apartment=comment.apartment,
            related_comment=comment
        )
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'status': 'success',
            'message': 'تم اعتماد التعليق بنجاح'
        })
    else:
        messages.success(request, 'تم اعتماد التعليق بنجاح')
        return redirect('apartment_detail', pk=comment.apartment.id)

@login_required
@require_POST
def reject_comment(request, comment_id):
    """رفض تعليق (للمسؤولين فقط)"""
    comment = get_object_or_404(Comment, pk=comment_id)
    
    # التحقق من أن المستخدم هو مسؤول
    if not request.user.is_staff:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'status': 'error',
                'message': 'ليس لديك صلاحية رفض التعليقات. هذه الصلاحية متاحة للمسؤولين فقط'
            })
        else:
            messages.error(request, 'ليس لديك صلاحية رفض التعليقات. هذه الصلاحية متاحة للمسؤولين فقط')
            return redirect('apartment_detail', pk=comment.apartment.id)
    
    comment.is_approved = False
    comment.save()
    
    # إنشاء إشعار لصاحب التعليق
    if request.user != comment.user:
        Notification.objects.create(
            user=comment.user,
            notification_type='new_comment',
            message=f'تم رفض تعليقك على شقة {comment.apartment.title}',
            related_apartment=comment.apartment,
            related_comment=comment
        )
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'status': 'success',
            'message': 'تم رفض التعليق بنجاح'
        })
    else:
        messages.success(request, 'تم رفض التعليق بنجاح')
        return redirect('apartment_detail', pk=comment.apartment.id)