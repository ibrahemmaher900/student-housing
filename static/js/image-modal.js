// فتح النافذة المنبثقة لعرض الصورة
function openImageModal(imgUrl, imgTitle) {
    const modalImage = document.getElementById('modalImage');
    const modalTitle = document.querySelector('#imageModal .modal-title');
    
    // تعيين مصدر الصورة والعنوان
    modalImage.src = imgUrl;
    modalTitle.textContent = imgTitle || 'صورة الشقة';
    
    // فتح النافذة المنبثقة
    const imageModal = new bootstrap.Modal(document.getElementById('imageModal'));
    imageModal.show();
}

// عند تحميل الصفحة
document.addEventListener('DOMContentLoaded', function() {
    // تهيئة الصور الرئيسية
    document.querySelectorAll('.main-image').forEach(img => {
        img.style.cursor = 'pointer';
        img.addEventListener('click', function() {
            const imgUrl = this.getAttribute('src');
            const imgTitle = this.getAttribute('alt') || 'صورة الشقة';
            openImageModal(imgUrl, imgTitle);
        });
    });
});