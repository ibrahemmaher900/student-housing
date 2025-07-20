/**
 * ملف JavaScript لتفعيل تأثيرات الحركة في جميع صفحات الموقع
 */

document.addEventListener('DOMContentLoaded', function() {
    // تفعيل تأثيرات الظهور عند التمرير
    const fadeElements = document.querySelectorAll('.fade-in');
    
    // تفعيل العناصر المرئية عند تحميل الصفحة
    fadeElements.forEach(element => {
        element.classList.add('active');
    });
    
    // تفعيل عداد الإحصائيات
    const statNumbers = document.querySelectorAll('.stat-number');
    
    if (statNumbers.length > 0) {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const target = parseInt(entry.target.getAttribute('data-count'));
                    const duration = 2000; // مدة العد بالمللي ثانية
                    const step = target / (duration / 16); // 16ms لكل إطار (60fps)
                    let current = 0;
                    
                    const updateCounter = () => {
                        current += step;
                        if (current < target) {
                            entry.target.textContent = Math.floor(current);
                            requestAnimationFrame(updateCounter);
                        } else {
                            entry.target.textContent = target;
                        }
                    };
                    
                    requestAnimationFrame(updateCounter);
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.5 });
        
        statNumbers.forEach(stat => {
            observer.observe(stat);
        });
    }
    
    // تفعيل تأثيرات التمرير السلس
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            const targetId = this.getAttribute('href');
            if (targetId !== '#' && document.querySelector(targetId)) {
                e.preventDefault();
                document.querySelector(targetId).scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });
    
    // تفعيل تأثيرات التحويم على البطاقات
    const cards = document.querySelectorAll('.card');
    cards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-10px)';
            this.style.boxShadow = '0 15px 30px rgba(0, 0, 0, 0.15)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = '';
            this.style.boxShadow = '';
        });
    });
});