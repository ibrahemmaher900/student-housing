// تحسينات الخريطة التفاعلية
let map, heatmapLayer, universityMarkers = [];
let isHeatmapActive = false;
let areUniversitiesVisible = false;

// تهيئة طبقة الخريطة الحرارية
function initHeatmap(apartments) {
    // تحويل بيانات الشقق إلى تنسيق مناسب للخريطة الحرارية
    const heatData = apartments.map(apt => {
        return [apt.latitude, apt.longitude, apt.price / 5000]; // تطبيع القيم حسب السعر
    });
    
    // إنشاء طبقة الخريطة الحرارية
    heatmapLayer = L.heatLayer(heatData, {
        radius: 25,
        blur: 15,
        maxZoom: 17,
        gradient: {
            0.4: 'blue',
            0.6: 'lime',
            0.8: 'yellow',
            1.0: 'red'
        }
    });
}

// تبديل عرض الخريطة الحرارية
function toggleHeatmap() {
    if (isHeatmapActive) {
        map.removeLayer(heatmapLayer);
        document.getElementById('toggle-heatmap').classList.replace('btn-success', 'btn-outline-success');
    } else {
        heatmapLayer.addTo(map);
        document.getElementById('toggle-heatmap').classList.replace('btn-outline-success', 'btn-success');
    }
    isHeatmapActive = !isHeatmapActive;
}

// إضافة مواقع الجامعات على الخريطة
function addUniversities(universityStats) {
    // إزالة العلامات الموجودة
    universityMarkers.forEach(marker => map.removeLayer(marker));
    universityMarkers = [];
    
    // إضافة علامات الجامعات
    for (const [uniName, stats] of Object.entries(universityStats)) {
        // هنا يجب أن تكون لديك إحداثيات الجامعات
        // هذا مثال افتراضي - في التطبيق الحقيقي يجب الحصول على الإحداثيات من قاعدة البيانات
        const marker = L.marker([24.7136 + Math.random() * 0.05, 46.6753 + Math.random() * 0.05], {
            icon: L.divIcon({
                className: 'university-marker',
                html: `<div class="uni-icon"><i class="fas fa-university"></i></div>`,
                iconSize: [40, 40]
            })
        });
        
        // إنشاء محتوى النافذة المنبثقة
        const popupContent = `
            <div class="university-popup">
                <h5>${uniName}</h5>
                <div class="uni-stats">
                    <div><i class="fas fa-home"></i> ${stats.count} شقة</div>
                    <div><i class="fas fa-money-bill"></i> ${Math.round(stats.avg_price)} ريال/شهر</div>
                </div>
            </div>
        `;
        
        marker.bindPopup(popupContent);
        universityMarkers.push(marker);
    }
}

// تبديل عرض الجامعات
function toggleUniversities() {
    if (areUniversitiesVisible) {
        universityMarkers.forEach(marker => map.removeLayer(marker));
        document.getElementById('toggle-universities').classList.replace('btn-info', 'btn-outline-info');
    } else {
        universityMarkers.forEach(marker => marker.addTo(map));
        document.getElementById('toggle-universities').classList.replace('btn-outline-info', 'btn-info');
    }
    areUniversitiesVisible = !areUniversitiesVisible;
}

// تهيئة أزرار التحكم
document.addEventListener('DOMContentLoaded', function() {
    // زر تبديل الخريطة الحرارية
    document.getElementById('toggle-heatmap').addEventListener('click', toggleHeatmap);
    
    // زر تبديل عرض الجامعات
    document.getElementById('toggle-universities').addEventListener('click', toggleUniversities);
    
    // زر الإحصائيات المتقدمة
    document.getElementById('toggle-stats').addEventListener('click', function() {
        const statsModal = new bootstrap.Modal(document.getElementById('statsModal'));
        statsModal.show();
    });
});