// ratings.js - وظائف JavaScript لنظام التقييمات

document.addEventListener('DOMContentLoaded', function() {
    // تحسين تجربة اختيار النجوم
    const ratingLabels = document.querySelectorAll('.rating-container label');
    
    ratingLabels.forEach(label => {
        label.addEventListener('mouseover', function() {
            // إضافة تأثير التحويم على النجوم
            const currentRating = this.getAttribute('for').split('_').pop();
            highlightStars(currentRating);
        });
        
        label.addEventListener('mouseout', function() {
            // إعادة تعيين النجوم إلى الحالة المحددة
            resetStars();
        });
    });
    
    // تحديد النجوم حتى النجمة التي تم التحويم عليها
    function highlightStars(rating) {
        ratingLabels.forEach(label => {
            const labelRating = label.getAttribute('for').split('_').pop();
            if (labelRating <= rating) {
                label.classList.add('hover');
            } else {
                label.classList.remove('hover');
            }
        });
    }
    
    // إعادة تعيين النجوم إلى الحالة المحددة
    function resetStars() {
        const checkedInput = document.querySelector('.rating-container input:checked');
        if (checkedInput) {
            const currentRating = checkedInput.value;
            highlightStars(currentRating);
        } else {
            ratingLabels.forEach(label => {
                label.classList.remove('hover');
            });
        }
    }
    
    // تفعيل أزرار الموافقة والرفض
    document.querySelectorAll('.approve-rating-btn, .reject-rating-btn').forEach(button => {
        button.addEventListener('click', function(e) {
            if (!confirm('هل أنت متأكد من تنفيذ هذا الإجراء؟')) {
                e.preventDefault();
            }
        });
    });
    
    // تحديث توزيع التقييمات في صفحة تفاصيل الشقة
    const ratingDistribution = document.querySelector('.rating-distribution');
    if (ratingDistribution) {
        // الحصول على جميع التقييمات من الصفحة
        const ratingItems = document.querySelectorAll('.rating-item');
        const totalRatings = ratingItems.length;
        
        // حساب عدد التقييمات لكل نجمة
        const ratingCounts = [0, 0, 0, 0, 0]; // للنجوم 1-5
        
        ratingItems.forEach(item => {
            const stars = item.querySelectorAll('.fa-star:not(.far)').length;
            if (stars >= 1 && stars <= 5) {
                ratingCounts[stars - 1]++;
            }
        });
        
        // تحديث أشرطة التقدم
        const ratingBars = ratingDistribution.querySelectorAll('.rating-bar');
        
        for (let i = 0; i < 5; i++) {
            const starCount = ratingCounts[4 - i]; // النجوم معروضة بترتيب تنازلي (5-1)
            const percentage = totalRatings > 0 ? (starCount / totalRatings) * 100 : 0;
            
            const progressBar = ratingBars[i].querySelector('.progress-bar');
            const countDisplay = ratingBars[i].querySelector('div:last-child');
            
            progressBar.style.width = `${percentage}%`;
            progressBar.setAttribute('aria-valuenow', percentage);
            countDisplay.textContent = starCount;
        }
    }
});