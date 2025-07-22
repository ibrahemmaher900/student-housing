// سكريبت بسيط لإرسال التقييم
document.addEventListener('DOMContentLoaded', function() {
    // التحقق من وجود نموذج التقييم
    const ratingForm = document.querySelector('form#rating-form');
    if (!ratingForm) return;
    
    // إضافة مستمع حدث للنموذج
    ratingForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        // جمع البيانات
        const formData = new FormData(ratingForm);
        
        // إرسال البيانات باستخدام fetch API
        fetch('/add-rating/', {
            method: 'POST',
            body: formData,
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                alert('تم إرسال تقييمك بنجاح!');
                window.location.href = '/';  // العودة إلى الصفحة الرئيسية
            } else {
                alert('حدث خطأ: ' + data.message);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('حدث خطأ أثناء إرسال التقييم');
        });
    });
});
