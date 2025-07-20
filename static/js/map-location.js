// map-location.js - وظائف JavaScript للخريطة وتحديد الموقع

document.addEventListener('DOMContentLoaded', function() {
    // تهيئة خريطة TomTom
    const apiKey = '7bpllxbhJJfYhMPF0WfVFzyVShKdQrpq';
    
    // موقع افتراضي (القاهرة)
    const defaultLat = 30.0444;
    const defaultLng = 31.2357;
    
    // إنشاء الخريطة
    const map = tt.map({
        key: apiKey,
        container: 'location-map',
        center: [defaultLng, defaultLat],
        zoom: 13
    });
    
    // إضافة أزرار التحكم
    map.addControl(new tt.NavigationControl());
    map.addControl(new tt.FullscreenControl());
    
    // إنشاء علامة قابلة للسحب
    const marker = new tt.Marker({
        draggable: true
    })
    .setLngLat([defaultLng, defaultLat])
    .addTo(map);
    
    // تحديث الإحداثيات عند سحب العلامة
    marker.on('dragend', function() {
        const lngLat = marker.getLngLat();
        document.getElementById('latitude').value = lngLat.lat.toFixed(6);
        document.getElementById('longitude').value = lngLat.lng.toFixed(6);
    });
    
    // تحديث الإحداثيات عند النقر على الخريطة
    map.on('click', function(e) {
        marker.setLngLat(e.lngLat);
        document.getElementById('latitude').value = e.lngLat.lat.toFixed(6);
        document.getElementById('longitude').value = e.lngLat.lng.toFixed(6);
    });
    
    // البحث عن العنوان وتحديد الموقع على الخريطة
    const searchAddressBtn = document.getElementById('search-address-btn');
    if (searchAddressBtn) {
        searchAddressBtn.addEventListener('click', function() {
            const city = document.getElementById('city-input').value;
            const district = document.getElementById('district-input').value;
            const address = document.getElementById('address-input').value;
            
            if (!city || !district || !address) {
                alert('يرجى إدخال المدينة والمنطقة والعنوان قبل البحث');
                return;
            }
            
            // إظهار مؤشر التحميل
            const searchSpinner = document.getElementById('search-spinner');
            searchSpinner.classList.remove('d-none');
            searchAddressBtn.disabled = true;
            
            // تكوين العنوان الكامل للبحث
            const fullAddress = `${address}, ${district}, ${city}, مصر`;
            
            // استخدام TomTom Fuzzy Search API للبحث عن العنوان
            tt.services.fuzzySearch({
                key: apiKey,
                query: fullAddress,
                limit: 1
            })
            .then(function(response) {
                // إعادة زر البحث إلى حالته الأصلية
                searchSpinner.classList.add('d-none');
                searchAddressBtn.disabled = false;
                
                if (response.results && response.results.length > 0) {
                    const result = response.results[0];
                    const position = result.position;
                    
                    // تحريك الخريطة إلى الموقع المعثور عليه
                    map.flyTo({
                        center: position,
                        zoom: 15
                    });
                    
                    // تحريك العلامة إلى الموقع المعثور عليه
                    marker.setLngLat(position);
                    
                    // تحديث حقول الإحداثيات
                    document.getElementById('latitude').value = position.lat.toFixed(6);
                    document.getElementById('longitude').value = position.lng.toFixed(6);
                    
                    // إظهار رسالة نجاح
                    alert('تم تحديد الموقع بنجاح!');
                } else {
                    alert('لم يتم العثور على العنوان. يرجى تحديد الموقع يدويًا على الخريطة.');
                }
            })
            .catch(function(error) {
                // إعادة زر البحث إلى حالته الأصلية
                searchSpinner.classList.add('d-none');
                searchAddressBtn.disabled = false;
                
                console.error('Error searching for address:', error);
                alert('حدث خطأ أثناء البحث عن العنوان. يرجى تحديد الموقع يدويًا على الخريطة.');
            });
        });
    }
    
    // تحديث الموقع تلقائيًا عند تغيير العنوان
    const addressInput = document.getElementById('address-input');
    if (addressInput) {
        addressInput.addEventListener('keydown', function(e) {
            if (e.key === 'Enter') {
                e.preventDefault(); // منع إرسال النموذج
                searchAddressBtn.click(); // تشغيل البحث
                return false;
            }
        });
    }
    
    // تحديث الموقع تلقائيًا عند تغيير المدينة أو المنطقة
    const cityInput = document.getElementById('city-input');
    const districtInput = document.getElementById('district-input');
    
    if (cityInput) {
        cityInput.addEventListener('change', function() {
            // التحقق من وجود قيم في جميع الحقول
            const city = this.value;
            const district = districtInput.value;
            const address = addressInput.value;
            
            if (city && district && address) {
                // تأخير البحث لتجنب البحث المتكرر
                setTimeout(() => {
                    searchAddressBtn.click();
                }, 500);
            }
        });
    }
    
    if (districtInput) {
        districtInput.addEventListener('change', function() {
            // التحقق من وجود قيم في جميع الحقول
            const city = cityInput.value;
            const district = this.value;
            const address = addressInput.value;
            
            if (city && district && address) {
                // تأخير البحث لتجنب البحث المتكرر
                setTimeout(() => {
                    searchAddressBtn.click();
                }, 500);
            }
        });
    }
});