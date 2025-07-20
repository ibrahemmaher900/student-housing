import bleach
from bleach.sanitizer import ALLOWED_TAGS, ALLOWED_ATTRIBUTES

def clean_html(html_content):
    """
    تنظيف محتوى HTML من العناصر الضارة
    """
    # تحديد العلامات المسموح بها
    allowed_tags = list(ALLOWED_TAGS) + ['p', 'br', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'img', 'hr']
    
    # تحديد السمات المسموح بها
    allowed_attrs = dict(ALLOWED_ATTRIBUTES)
    allowed_attrs['img'] = ['src', 'alt', 'title', 'width', 'height']
    
    # تنظيف المحتوى
    cleaned_content = bleach.clean(
        html_content,
        tags=allowed_tags,
        attributes=allowed_attrs,
        strip=True
    )
    
    return cleaned_content

def clean_text(text):
    """
    تنظيف النص العادي من أي محتوى HTML
    """
    return bleach.clean(text, tags=[], strip=True)