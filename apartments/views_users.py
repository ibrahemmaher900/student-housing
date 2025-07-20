from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User

def is_admin(user):
    return user.is_staff or user.is_superuser

@login_required
@user_passes_test(is_admin)
def admin_users(request):
    """صفحة إدارة المستخدمين للمسؤولين"""
    # الحصول على جميع المستخدمين
    users = User.objects.all().select_related('profile')
    
    # تقسيم المستخدمين حسب النوع
    students = [user for user in users if user.profile.user_type == 'student']
    owners = [user for user in users if user.profile.user_type == 'owner']
    
    # المستخدمين المحظورين
    banned_users = [user for user in users if hasattr(user, 'profile') and user.profile.is_banned]
    
    # المستخدمين المبلغ عنهم (لديهم إبلاغات ولكن لم يتم حظرهم بعد)
    reported_users = [user for user in users if hasattr(user, 'profile') and user.profile.non_serious_reports > 0 and not user.profile.is_banned]
    
    context = {
        'users': users,
        'students': students,
        'owners': owners,
        'banned_users': banned_users,
        'reported_users': reported_users,
    }
    return render(request, 'apartments/admin_users.html', context)