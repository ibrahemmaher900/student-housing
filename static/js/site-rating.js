// نافذة تقييم الموقع
document.addEventListener('DOMContentLoaded', function() {
    // التحقق من وجود المستخدم وعدم ظهور النافذة من قبل
    const hasRated = localStorage.getItem('site_rated');
    const isAuthenticated = document.body.classList.contains('user-authenticated');
    
    if (isAuthenticated && !hasRated) {
        // عرض النافذة بعد 60 ثانية من تصفح الموقع
        setTimeout(() => {
            const ratingModal = new bootstrap.Modal(document.getElementById('ratingModal'));
            ratingModal.show();
        }, 60000); // 60 ثانية
    }
    
    // حفظ التقييم وإغلاق النافذة
    document.getElementById('submitRating').addEventListener('click', function() {
        const rating = document.querySelector('input[name="rating"]:checked')?.value;
        const review = document.getElementById('reviewText').value;
        
        if (rating) {
            // إرسال التقييم إلى الخادم
            fetch('/submit-rating/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify({
                    rating: rating,
                    review: review
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    // تخزين أن المستخدم قام بالتقييم
                    localStorage.setItem('site_rated', 'true');
                    
                    // إظهار رسالة شكر
                    const thankYouAlert = document.createElement('div');
                    thankYouAlert.className = 'alert alert-success alert-dismissible fade show';
                    thankYouAlert.innerHTML = `
                        شكراً لتقييمك! سيساعدنا ذلك في تحسين خدماتنا.
                        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                    `;
                    document.querySelector('.container').prepend(thankYouAlert);
                    
                    // إغلاق النافذة
                    bootstrap.Modal.getInstance(document.getElementById('ratingModal')).hide();
                    
                    // إخفاء الرسالة بعد 5 ثواني
                    setTimeout(() => {
                        thankYouAlert.remove();
                    }, 5000);
                }
            });
        }
    });
    
    // دالة للحصول على قيمة الكوكي
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