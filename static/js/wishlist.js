document.addEventListener('DOMContentLoaded', function() {
    // الحصول على جميع أزرار المفضلة
    const wishlistButtons = document.querySelectorAll('.wishlist-btn');
    
    // إضافة مستمع حدث لكل زر
    wishlistButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            
            // التحقق من تسجيل الدخول
            if (!document.body.classList.contains('user-authenticated')) {
                window.location.href = '/users/login/';
                return;
            }
            
            const apartmentId = this.getAttribute('data-id');
            const isInWishlist = this.getAttribute('data-in-wishlist') === 'true';
            const heartIcon = this.querySelector('i');
            
            // إرسال طلب AJAX لتبديل حالة المفضلة
            fetch(`/apartments/${apartmentId}/wishlist/`, {
                method: 'GET',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'Content-Type': 'application/json'
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    // تحديث جميع أزرار المفضلة لنفس الشقة
                    document.querySelectorAll(`.wishlist-btn[data-id="${apartmentId}"]`).forEach(btn => {
                        btn.setAttribute('data-in-wishlist', data.is_in_wishlist);
                        const btnIcon = btn.querySelector('i');
                        if (data.is_in_wishlist) {
                            btnIcon.classList.remove('far');
                            btnIcon.classList.add('fas');
                            btnIcon.style.color = 'red';
                        } else {
                            btnIcon.classList.remove('fas');
                            btnIcon.classList.add('far');
                            btnIcon.style.color = '';
                        }
                    });
                    
                    // عرض رسالة للمستخدم
                    const toast = document.createElement('div');
                    toast.className = 'position-fixed bottom-0 end-0 p-3';
                    toast.style.zIndex = '5';
                    toast.innerHTML = `
                        <div class="toast align-items-center text-white bg-${data.is_in_wishlist ? 'success' : 'primary'} border-0" role="alert" aria-live="assertive" aria-atomic="true">
                            <div class="d-flex">
                                <div class="toast-body">
                                    <i class="fas fa-${data.is_in_wishlist ? 'check-circle' : 'info-circle'} me-2"></i>
                                    ${data.message}
                                </div>
                                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
                            </div>
                        </div>
                    `;
                    document.body.appendChild(toast);
                    
                    // تفعيل التنبيه
                    const toastElement = toast.querySelector('.toast');
                    const bsToast = new bootstrap.Toast(toastElement, { delay: 3000 });
                    bsToast.show();
                    
                    // إزالة التنبيه بعد إخفائه
                    toastElement.addEventListener('hidden.bs.toast', function() {
                        toast.remove();
                    });
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
        });
    });
});