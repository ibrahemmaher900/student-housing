// comments.js - وظائف JavaScript لنظام التعليقات

document.addEventListener('DOMContentLoaded', function() {
    // تفعيل نموذج التعليق المباشر
    const commentForm = document.getElementById('comment-form');
    if (commentForm) {
        commentForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const formData = new FormData(commentForm);
            const url = commentForm.getAttribute('action');
            
            fetch(url, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    // إعادة تحميل الصفحة لعرض التعليق الجديد
                    window.location.reload();
                } else {
                    // عرض رسالة الخطأ
                    alert(data.message || 'حدث خطأ أثناء إضافة التعليق');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('حدث خطأ أثناء إضافة التعليق');
            });
        });
    }
    
    // تفعيل أزرار الموافقة والرفض
    document.querySelectorAll('.approve-comment-btn, .reject-comment-btn').forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            
            const url = this.getAttribute('href');
            
            fetch(url, {
                method: 'POST',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': getCookie('csrftoken')
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    // إعادة تحميل الصفحة لتحديث حالة التعليق
                    window.location.reload();
                } else {
                    // عرض رسالة الخطأ
                    alert(data.message || 'حدث خطأ أثناء تحديث حالة التعليق');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('حدث خطأ أثناء تحديث حالة التعليق');
            });
        });
    });
    
    // دالة للحصول على قيمة ملف تعريف الارتباط
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});