// تغيير العملة من ريال سعودي إلى جنيه مصري
document.addEventListener('DOMContentLoaded', function() {
    // تغيير النص في جميع العناصر التي تحتوي على "ر.س"
    document.querySelectorAll('*').forEach(function(element) {
        if (element.childNodes && element.childNodes.length > 0) {
            element.childNodes.forEach(function(node) {
                if (node.nodeType === 3) { // نوع النص
                    node.textContent = node.textContent
                        .replace(/ر\.س/g, 'ج.م')
                        .replace(/ريال/g, 'جنيه')
                        .replace(/SAR/g, 'EGP');
                }
            });
        }
    });
});
