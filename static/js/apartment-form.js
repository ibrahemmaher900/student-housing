// متغيرات عامة
var currentSection = 1;
var totalSections = 5;
var map;
var marker;

// تنفيذ الكود عند تحميل الصفحة
document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM loaded - Apartment Form');
    initFormNavigation();
});

// تهيئة التنقل بين أقسام النموذج
function initFormNavigation() {
    // أزرار التنقل
    var prevBtn = document.getElementById('prevBtn');
    var nextBtn = document.getElementById('nextBtn');
    
    // زر السابق
    if (prevBtn) {
        prevBtn.addEventListener('click', function() {
            if (currentSection > 1) {
                currentSection--;
                showSection(currentSection);
                updateProgressBar();
            }
        });
    }
    
    // زر التالي
    if (nextBtn) {
        nextBtn.addEventListener('click', function() {
            console.log('Next button clicked');
            if (currentSection < totalSections) {
                currentSection++;
                showSection(currentSection);
                updateProgressBar();
            }
        });
    }
    
    // تهيئة الخطوات
    for (var i = 1; i <= totalSections; i++) {
        (function(stepNum) {
            var stepItem = document.getElementById('step' + stepNum);
            if (stepItem) {
                stepItem.style.cursor = 'pointer';
                stepItem.addEventListener('click', function() {
                    currentSection = stepNum;
                    showSection(currentSection);
                    updateProgressBar();
                });
            }
        })(i);
    }
    
    // إظهار القسم الأول
    showSection(currentSection);
    updateProgressBar();
    
    // تهيئة الخريطة
    setTimeout(function() {
        initMap();
    }, 500);
    
    // تهيئة معاينة الصور
    setupImagePreview();
}

// إظهار القسم المحدد وإخفاء باقي الأقسام
function showSection(sectionNumber) {
    console.log('Showing section:', sectionNumber);
    
    // إخفاء جميع الأقسام
    for (var i = 1; i <= totalSections; i++) {
        var section = document.getElementById('section' + i);
        if (section) {
            section.style.display = 'none';
        }
    }
    
    // إظهار القسم الحالي
    var currentSectionElement = document.getElementById('section' + sectionNumber);
    if (currentSectionElement) {
        currentSectionElement.style.display = 'block';
    }
    
    // تحديث حالة الأزرار
    var prevBtn = document.getElementById('prevBtn');
    var nextBtn = document.getElementById('nextBtn');
    var submitBtn = document.getElementById('submitBtn');
    
    if (prevBtn) {
        prevBtn.disabled = (sectionNumber === 1);
    }
    
    if (nextBtn && submitBtn) {
        if (sectionNumber === totalSections) {
            nextBtn.style.display = 'none';
            submitBtn.style.display = 'block';
        } else {
            nextBtn.style.display = 'block';
            submitBtn.style.display = 'none';
        }
    }
    
    // تحديث حجم الخريطة إذا كان القسم الحالي هو قسم الموقع
    if (sectionNumber === 3 && map) {
        setTimeout(function() {
            map.invalidateSize();
        }, 100);
    }
    
    // تحديث حالة الخطوات
    updateSteps(sectionNumber);
}

// تحديث شريط التقدم
function updateProgressBar() {
    var progressBar = document.getElementById('formProgress');
    if (progressBar) {
        var progress = (currentSection - 1) / (totalSections - 1) * 100;
        progressBar.style.width = progress + '%';
    }
}

// تحديث حالة الخطوات
function updateSteps(currentStep) {
    // إزالة جميع الفئات النشطة والمكتملة
    for (var i = 1; i <= totalSections; i++) {
        var stepCircle = document.querySelector('#step' + i + ' .step-circle');
        if (stepCircle) {
            stepCircle.classList.remove('active', 'completed');
        }
    }
    
    // تعيين الخطوات المكتملة والنشطة
    for (var i = 1; i <= totalSections; i++) {
        var stepCircle = document.querySelector('#step' + i + ' .step-circle');
        if (stepCircle) {
            if (i < currentStep) {
                stepCircle.classList.add('completed');
            } else if (i === currentStep) {
                stepCircle.classList.add('active');
            }
        }
    }
}

// إعداد معاينة الصور
function setupImagePreview() {
    var imageInput = document.getElementById('id_image');
    var imagePreview = document.getElementById('imagePreview');
    
    if (imageInput && imagePreview) {
        imageInput.addEventListener('change', function() {
            imagePreview.innerHTML = '';
            
            if (this.files && this.files.length > 0) {
                var row = document.createElement('div');
                row.className = 'row g-3';
                imagePreview.appendChild(row);
                
                for (var i = 0; i < this.files.length; i++) {
                    var file = this.files[i];
                    if (!file.type.match('image.*')) continue;
                    
                    var reader = new FileReader();
                    (function(idx) {
                        reader.onload = function(e) {
                            var col = document.createElement('div');
                            col.className = 'col-md-3 col-6';
                            
                            var card = document.createElement('div');
                            card.className = 'card h-100';
                            
                            var img = document.createElement('img');
                            img.src = e.target.result;
                            img.className = 'card-img-top';
                            img.style.height = '150px';
                            img.style.objectFit = 'cover';
                            
                            var cardBody = document.createElement('div');
                            cardBody.className = 'card-body p-2 text-center';
                            cardBody.innerHTML = '<small class="text-muted">صورة ' + (idx+1) + '</small>';
                            
                            card.appendChild(img);
                            card.appendChild(cardBody);
                            col.appendChild(card);
                            row.appendChild(col);
                        };
                    })(i);
                    
                    reader.readAsDataURL(file);
                }
            }
        });
    }
}

// تهيئة الخريطة
function initMap() {
    try {
        var mapElement = document.getElementById('map');
        if (!mapElement) return;
        
        // إحداثيات افتراضية (الرياض)
        var defaultLat = (typeof mapSettings !== 'undefined') ? mapSettings.defaultLat : 24.7136;
        var defaultLng = (typeof mapSettings !== 'undefined') ? mapSettings.defaultLng : 46.6753;
        var defaultZoom = (typeof mapSettings !== 'undefined') ? mapSettings.defaultZoom : 10;
        
        // التحقق من وجود إحداثيات محفوظة
        var latField = document.getElementById('id_latitude');
        var lngField = document.getElementById('id_longitude');
        
        var center = { lat: defaultLat, lng: defaultLng };
        if (latField && latField.value && lngField && lngField.value) {
            center = {
                lat: parseFloat(latField.value),
                lng: parseFloat(lngField.value)
            };
        }
        
        // إنشاء الخريطة
        map = L.map('map').setView([center.lat, center.lng], defaultZoom);
        
        // إضافة طبقة OpenStreetMap
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
            maxZoom: 19
        }).addTo(map);
        
        // إضافة علامة إذا كانت هناك إحداثيات محفوظة
        if (latField && latField.value && lngField && lngField.value) {
            marker = L.marker([center.lat, center.lng], {
                draggable: true
            }).addTo(map);
            
            // تحديث الإحداثيات عند سحب العلامة
            marker.on('dragend', function() {
                var position = marker.getLatLng();
                updateCoordinates(position);
            });
        }
        
        // إضافة حدث النقر على الخريطة
        map.on('click', function(event) {
            placeMarker(event.latlng);
        });
        
        // إضافة حدث للبحث عن موقع
        var searchBtn = document.getElementById('searchBtn');
        var searchInput = document.getElementById('searchLocation');
        
        if (searchBtn && searchInput) {
            searchBtn.addEventListener('click', function() {
                var query = searchInput.value;
                if (query) {
                    searchLocation(query);
                }
            });
            
            searchInput.addEventListener('keypress', function(e) {
                if (e.key === 'Enter') {
                    e.preventDefault();
                    var query = searchInput.value;
                    if (query) {
                        searchLocation(query);
                    }
                }
            });
        }
        
        // إضافة حدث للحصول على الموقع الحالي
        var getCurrentLocationBtn = document.getElementById('getCurrentLocation');
        if (getCurrentLocationBtn) {
            getCurrentLocationBtn.addEventListener('click', function() {
                if (navigator.geolocation) {
                    navigator.geolocation.getCurrentPosition(function(position) {
                        var location = {
                            lat: position.coords.latitude,
                            lng: position.coords.longitude
                        };
                        map.setView([location.lat, location.lng], 15);
                        placeMarker(location);
                    }, function() {
                        alert('تعذر الوصول إلى موقعك الحالي.');
                    });
                } else {
                    alert('متصفحك لا يدعم تحديد الموقع الجغرافي.');
                }
            });
        }
    } catch (e) {
        console.error("Error initializing map:", e);
    }
}

// البحث عن موقع
function searchLocation(query) {
    // استخدام Nominatim API للبحث عن الموقع
    fetch(`https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(query)}`)
        .then(response => response.json())
        .then(data => {
            if (data && data.length > 0) {
                var location = {
                    lat: parseFloat(data[0].lat),
                    lng: parseFloat(data[0].lon)
                };
                
                map.setView([location.lat, location.lng], 15);
                placeMarker(location);
            } else {
                alert('لم يتم العثور على الموقع. يرجى المحاولة باستخدام عبارة أخرى.');
            }
        })
        .catch(error => {
            console.error('Error searching location:', error);
            alert('حدث خطأ أثناء البحث عن الموقع.');
        });
}

// وضع علامة على الخريطة
function placeMarker(location) {
    try {
        if (marker) {
            marker.setLatLng(location);
        } else {
            marker = L.marker(location, {
                draggable: true
            }).addTo(map);
            
            // تحديث الإحداثيات عند سحب العلامة
            marker.on('dragend', function() {
                var position = marker.getLatLng();
                updateCoordinates(position);
            });
        }
        
        updateCoordinates(location);
    } catch (e) {
        console.error("Error placing marker:", e);
    }
}

// تحديث حقول الإحداثيات
function updateCoordinates(location) {
    var latField = document.getElementById('id_latitude');
    var lngField = document.getElementById('id_longitude');
    
    if (latField && lngField) {
        latField.value = location.lat.toFixed(6);
        lngField.value = location.lng.toFixed(6);
    }
}