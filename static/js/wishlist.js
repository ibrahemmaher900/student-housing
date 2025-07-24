document.addEventListener('DOMContentLoaded', function() {
    // التعامل مع أزرار المفضلات
    const wishlistButtons = document.querySelectorAll('.wishlist-btn');
    
    wishlistButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            
            const apartmentId = this.dataset.id;
            const isInWishlist = this.dataset.inWishlist === 'true';
            
            // إرسال طلب AJAX
            fetch(`/apartments/${apartmentId}/toggle-wishlist/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                    'X-Requested-With': 'XMLHttpRequest',
                    'Content-Type': 'application/json',
                },
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    const icon = this.querySelector('i');
                    
                    if (data.is_in_wishlist) {
                        icon.className = 'fas fa-heart';
                        icon.style.color = 'red';
                        this.dataset.inWishlist = 'true';
                    } else {
                        icon.className = 'far fa-heart';
                        icon.style.color = '';
                        this.dataset.inWishlist = 'false';
                    }
                    
                    // إظهار رسالة نجاح
                    showMessage(data.message, 'success');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showMessage('حدث خطأ أثناء تحديث المفضلات', 'error');
            });
        });
    });
});

// دالة للحصول على قيمة الكوكيز
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

// دالة لإظهار الرسائل
function showMessage(message, type) {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type === 'success' ? 'success' : 'danger'} alert-dismissible fade show`;
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    const container = document.querySelector('.container');
    if (container) {
        container.insertBefore(alertDiv, container.firstChild);
        
        // إزالة الرسالة تلقائياً بعد 3 ثوان
        setTimeout(() => {
            alertDiv.remove();
        }, 3000);
    }
}