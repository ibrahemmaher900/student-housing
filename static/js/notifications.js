// نظام الإشعارات المحسن
document.addEventListener('DOMContentLoaded', function() {
    // تحديث عداد الإشعارات كل دقيقة
    setInterval(updateNotificationsCount, 60000);
    
    // تهيئة قائمة الإشعارات المنسدلة
    initNotificationsDropdown();
    
    // تهيئة زر تحديث الإشعارات
    initRefreshButton();
    
    // تحديث وقت الإشعارات (منذ متى)
    updateNotificationTimes();
    setInterval(updateNotificationTimes, 60000);
});

// تحديث عدد الإشعارات غير المقروءة
function updateNotificationsCount() {
    fetch('/apartments/notifications/count/')
        .then(response => response.json())
        .then(data => {
            const badge = document.getElementById('notifications-badge');
            if (badge) {
                if (data.count > 0) {
                    badge.textContent = data.count;
                    badge.style.display = 'inline-block';
                    
                    // إضافة تأثير وميض للإشعارات الجديدة
                    if (!badge.classList.contains('pulse-animation')) {
                        badge.classList.add('pulse-animation');
                        setTimeout(() => {
                            badge.classList.remove('pulse-animation');
                        }, 2000);
                    }
                } else {
                    badge.style.display = 'none';
                }
            }
        })
        .catch(error => console.error('خطأ في تحديث الإشعارات:', error));
}

// تهيئة قائمة الإشعارات المنسدلة
function initNotificationsDropdown() {
    const notificationItems = document.querySelectorAll('.notification-item');
    
    notificationItems.forEach(item => {
        // تعليم الإشعار كمقروء عند النقر عليه
        item.addEventListener('click', function(e) {
            // تجاهل النقر على أزرار الإجراءات
            if (e.target.closest('.notification-actions')) {
                return;
            }
            
            const notificationId = this.dataset.id;
            if (notificationId) {
                markAsRead(notificationId);
            }
        });
    });
}

// تهيئة زر تحديث الإشعارات
function initRefreshButton() {
    const refreshButton = document.getElementById('refresh-notifications');
    if (refreshButton) {
        refreshButton.addEventListener('click', function() {
            // إضافة تأثير دوران للزر
            this.classList.add('fa-spin');
            
            // تحديث الإشعارات
            fetch('/apartments/notifications/recent/')
                .then(response => response.json())
                .then(data => {
                    const container = document.getElementById('notifications-container');
                    if (container && data.html) {
                        container.innerHTML = data.html;
                        initNotificationsDropdown(); // إعادة تهيئة الأحداث
                    }
                    
                    // تحديث العداد
                    updateNotificationsCount();
                })
                .catch(error => console.error('خطأ في تحديث الإشعارات:', error))
                .finally(() => {
                    // إزالة تأثير الدوران بعد ثانية
                    setTimeout(() => {
                        refreshButton.classList.remove('fa-spin');
                    }, 1000);
                });
        });
    }
}

// تعليم الإشعار كمقروء
function markAsRead(notificationId) {
    // الحصول على رمز CSRF
    const csrfToken = getCsrfToken();
    
    fetch(`/apartments/notifications/${notificationId}/read/api/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrfToken,
            'Content-Type': 'application/json',
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // تحديث مظهر الإشعار
            const notificationItem = document.querySelector(`.notification-item[data-id="${notificationId}"]`);
            if (notificationItem) {
                notificationItem.classList.remove('unread');
                const unreadBadge = notificationItem.querySelector('.badge.bg-danger');
                if (unreadBadge) {
                    unreadBadge.remove();
                }
            }
            // تحديث عداد الإشعارات
            updateNotificationsCount();
            // إعادة التوجيه إذا تم إرجاع رابط
            if (data.redirect_url) {
                window.location.href = data.redirect_url;
            }
        }
    })
    .catch(error => console.error('خطأ في تعليم الإشعار كمقروء:', error));
}

// تحديث أوقات الإشعارات (منذ متى)
function updateNotificationTimes() {
    const timeElements = document.querySelectorAll('.notification-time');
    timeElements.forEach(element => {
        const timestamp = parseInt(element.dataset.timestamp);
        if (timestamp) {
            element.textContent = timeAgo(timestamp);
        }
    });
}

// دالة لحساب الوقت المنقضي
function timeAgo(timestamp) {
    const now = new Date().getTime();
    const seconds = Math.floor((now - timestamp) / 1000);
    
    let interval = Math.floor(seconds / 31536000);
    if (interval > 1) return `منذ ${interval} سنة`;
    if (interval === 1) return 'منذ سنة';
    
    interval = Math.floor(seconds / 2592000);
    if (interval > 1) return `منذ ${interval} شهر`;
    if (interval === 1) return 'منذ شهر';
    
    interval = Math.floor(seconds / 86400);
    if (interval > 1) return `منذ ${interval} يوم`;
    if (interval === 1) return 'منذ يوم';
    
    interval = Math.floor(seconds / 3600);
    if (interval > 1) return `منذ ${interval} ساعة`;
    if (interval === 1) return 'منذ ساعة';
    
    interval = Math.floor(seconds / 60);
    if (interval > 1) return `منذ ${interval} دقيقة`;
    if (interval === 1) return 'منذ دقيقة';
    
    return 'الآن';
}

// الحصول على رمز CSRF
function getCsrfToken() {
    const csrfCookie = document.cookie.split(';')
        .find(cookie => cookie.trim().startsWith('csrftoken='));
    
    if (csrfCookie) {
        return csrfCookie.split('=')[1];
    }
    
    // البحث عن الرمز في عناصر الصفحة
    const csrfInput = document.querySelector('[name=csrfmiddlewaretoken]');
    if (csrfInput) {
        return csrfInput.value;
    }
    
    return '';
}