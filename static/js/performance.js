// تحسينات الأداء للواجهة الأمامية
document.addEventListener('DOMContentLoaded', function() {
    
    // 1. تحسين النماذج - منع الإرسال المتكرر
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        let isSubmitting = false;
        
        form.addEventListener('submit', function(e) {
            if (isSubmitting) {
                e.preventDefault();
                return false;
            }
            
            isSubmitting = true;
            const submitBtn = form.querySelector('button[type="submit"]');
            
            if (submitBtn) {
                const originalText = submitBtn.innerHTML;
                submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>جاري المعالجة...';
                submitBtn.disabled = true;
                
                // إعادة تفعيل الزر بعد 10 ثوان كحد أقصى
                setTimeout(() => {
                    submitBtn.innerHTML = originalText;
                    submitBtn.disabled = false;
                    isSubmitting = false;
                }, 10000);
            }
        });
    });

    // 2. تحسين الصور - تحميل تدريجي
    const images = document.querySelectorAll('img');
    images.forEach(img => {
        if (!img.complete) {
            img.style.opacity = '0';
            img.addEventListener('load', function() {
                this.style.transition = 'opacity 0.3s';
                this.style.opacity = '1';
            });
        }
    });

    // 3. تحسين AJAX - إضافة timeout
    const originalFetch = window.fetch;
    window.fetch = function(...args) {
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), 10000); // 10 ثوان timeout
        
        const options = args[1] || {};
        options.signal = controller.signal;
        args[1] = options;
        
        return originalFetch.apply(this, args)
            .finally(() => clearTimeout(timeoutId));
    };

    // 4. تحسين التمرير - throttling
    let ticking = false;
    function updateScrollElements() {
        // تحديث العناصر المرتبطة بالتمرير
        ticking = false;
    }
    
    window.addEventListener('scroll', function() {
        if (!ticking) {
            requestAnimationFrame(updateScrollElements);
            ticking = true;
        }
    });

    // 5. تحسين تغيير الحجم
    let resizeTimeout;
    window.addEventListener('resize', function() {
        clearTimeout(resizeTimeout);
        resizeTimeout = setTimeout(function() {
            // إعادة حساب التخطيط
            window.dispatchEvent(new Event('optimizedResize'));
        }, 250);
    });

    // 6. تحسين النقرات - debouncing
    function debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }

    // تطبيق debouncing على أزرار البحث
    const searchButtons = document.querySelectorAll('button[type="submit"]');
    searchButtons.forEach(btn => {
        const originalClick = btn.onclick;
        btn.onclick = debounce(originalClick || function(){}, 300);
    });

    // 7. تحسين الذاكرة - تنظيف المستمعين
    window.addEventListener('beforeunload', function() {
        // تنظيف المستمعين والمؤقتات
        forms.forEach(form => {
            form.removeEventListener('submit', arguments.callee);
        });
    });

    // 8. تحسين التحميل - preload للروابط المهمة
    const importantLinks = document.querySelectorAll('a[href^="/apartments/"]');
    importantLinks.forEach(link => {
        link.addEventListener('mouseenter', function() {
            const linkElement = document.createElement('link');
            linkElement.rel = 'prefetch';
            linkElement.href = this.href;
            document.head.appendChild(linkElement);
        }, { once: true });
    });
});

// دالة لقياس الأداء
function measurePerformance() {
    if ('performance' in window) {
        const navigation = performance.getEntriesByType('navigation')[0];
        const loadTime = navigation.loadEventEnd - navigation.loadEventStart;
        
        console.log(`Page load time: ${loadTime}ms`);
        
        // إرسال البيانات للخادم إذا كان التحميل بطيئاً
        if (loadTime > 3000) {
            fetch('/performance-report/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify({
                    loadTime: loadTime,
                    url: window.location.href
                })
            }).catch(() => {}); // تجاهل الأخطاء
        }
    }
}

// قياس الأداء بعد تحميل الصفحة
window.addEventListener('load', measurePerformance);

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