document.addEventListener('DOMContentLoaded', function() {
    // تهيئة مكتبة AOS للتأثيرات الحركية
    AOS.init({
        duration: 800,
        easing: 'ease-in-out',
        once: true
    });
    
    // إضافة تأثيرات حركية للأقسام
    document.querySelectorAll('.detail-section').forEach((section, index) => {
        section.setAttribute('data-aos', 'fade-up');
        section.setAttribute('data-aos-delay', (index * 100).toString());
    });
    
    // تهيئة معرض الصور الرئيسي
    const swiperThumbs = new Swiper('.apartment-thumbs', {
        spaceBetween: 10,
        slidesPerView: 'auto',
        freeMode: true,
        watchSlidesProgress: true,
    });
    
    const swiperMain = new Swiper('.apartment-gallery', {
        spaceBetween: 10,
        navigation: {
            nextEl: '.swiper-button-next',
            prevEl: '.swiper-button-prev',
        },
        pagination: {
            el: '.swiper-pagination',
            clickable: true,
        },
        thumbs: {
            swiper: swiperThumbs,
        },
    });
    
    // تهيئة Lightbox
    lightbox.option({
        'resizeDuration': 200,
        'wrapAround': true,
        'albumLabel': 'صورة %1 من %2',
        'fadeDuration': 300
    });
    
    // تهيئة الخريطة
    if (document.getElementById('map')) {
        const mapElement = document.getElementById('map');
        const lat = parseFloat(mapElement.getAttribute('data-lat'));
        const lng = parseFloat(mapElement.getAttribute('data-lng'));
        
        if (lat && lng) {
            const map = L.map('map').setView([lat, lng], 15);
            
            L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
                maxZoom: 19
            }).addTo(map);
            
            // إضافة علامة للشقة
            const marker = L.marker([lat, lng]).addTo(map);
            
            // تحسين تجربة المستخدم مع الخريطة
            setTimeout(() => {
                map.invalidateSize();
            }, 300);
        }
    }
    
    // نسخ رابط المشاركة
    document.querySelectorAll('.copy-link').forEach(button => {
        button.addEventListener('click', function() {
            const url = this.getAttribute('data-url');
            navigator.clipboard.writeText(url).then(() => {
                // إظهار رسالة نجاح
                const toast = document.createElement('div');
                toast.className = 'position-fixed bottom-0 end-0 p-3';
                toast.style.zIndex = '5';
                toast.innerHTML = `
                    <div class="toast align-items-center text-white bg-success border-0" role="alert" aria-live="assertive" aria-atomic="true">
                        <div class="d-flex">
                            <div class="toast-body">
                                <i class="fas fa-check-circle me-2"></i>
                                تم نسخ الرابط بنجاح!
                            </div>
                            <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
                        </div>
                    </div>
                `;
                document.body.appendChild(toast);
                
                const toastElement = toast.querySelector('.toast');
                const bsToast = new bootstrap.Toast(toastElement, { delay: 3000 });
                bsToast.show();
                
                toastElement.addEventListener('hidden.bs.toast', function() {
                    toast.remove();
                });
            });
        });
    });
    
    // تفعيل التبويبات
    const tabTriggers = document.querySelectorAll('.apartment-tab-trigger');
    tabTriggers.forEach(trigger => {
        trigger.addEventListener('click', function(e) {
            e.preventDefault();
            
            // إزالة الفئة النشطة من جميع الأزرار
            tabTriggers.forEach(t => t.classList.remove('active'));
            
            // إضافة الفئة النشطة للزر الحالي
            this.classList.add('active');
            
            // إخفاء جميع المحتويات
            document.querySelectorAll('.apartment-tab-content').forEach(content => {
                content.classList.add('d-none');
            });
            
            // إظهار المحتوى المطلوب
            const targetId = this.getAttribute('data-target');
            document.getElementById(targetId).classList.remove('d-none');
        });
    });
});