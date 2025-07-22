document.addEventListener('DOMContentLoaded', function() {
    // العثور على نموذج التقييم
    const ratingForm = document.getElementById('rating-form');
    
    if (ratingForm) {
        ratingForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            // الحصول على بيانات النموذج
            const rating = document.querySelector('input[name="rating"]:checked')?.value;
            const comment = document.querySelector('textarea[name="comment"]').value;
            
            // التحقق من البيانات
            if (!rating) {
                alert('يرجى اختيار تقييم');
                return;
            }
            
            // إنشاء طلب AJAX
            const xhr = new XMLHttpRequest();
            xhr.open('POST', '/add-rating/');
            xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
            xhr.setRequestHeader('X-CSRFToken', getCookie('csrftoken'));
            
            xhr.onload = function() {
                if (xhr.status === 200) {
                    const response = JSON.parse(xhr.responseText);
                    if (response.status === 'success') {
                        alert('تم إرسال تقييمك بنجاح');
                        // إعادة تحميل الصفحة أو إغلاق النافذة المنبثقة
                        window.location.reload();
                    } else {
                        alert('حدث خطأ: ' + response.message);
                    }
                } else {
                    alert('حدث خطأ في الاتصال بالخادم');
                }
            };
            
            xhr.onerror = function() {
                alert('حدث خطأ في الاتصال بالخادم');
            };
            
            // إرسال البيانات
            xhr.send('rating=' + encodeURIComponent(rating) + '&comment=' + encodeURIComponent(comment));
        });
    }
    
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
