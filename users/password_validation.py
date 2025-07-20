import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

class PasswordValidator:
    """
    التحقق من قوة كلمة المرور
    """
    
    def __init__(self, min_length=10):
        self.min_length = min_length
    
    def validate(self, password, user=None):
        """
        التحقق من قوة كلمة المرور
        """
        # التحقق من الطول الأدنى
        if len(password) < self.min_length:
            raise ValidationError(
                _("يجب أن تتكون كلمة المرور من %(min_length)d حرف على الأقل."),
                code='password_too_short',
                params={'min_length': self.min_length},
            )
        
        # التحقق من وجود حرف كبير
        if not re.search(r'[A-Z]', password):
            raise ValidationError(
                _("يجب أن تحتوي كلمة المرور على حرف كبير واحد على الأقل."),
                code='password_no_upper',
            )
        
        # التحقق من وجود حرف صغير
        if not re.search(r'[a-z]', password):
            raise ValidationError(
                _("يجب أن تحتوي كلمة المرور على حرف صغير واحد على الأقل."),
                code='password_no_lower',
            )
        
        # التحقق من وجود رقم
        if not re.search(r'[0-9]', password):
            raise ValidationError(
                _("يجب أن تحتوي كلمة المرور على رقم واحد على الأقل."),
                code='password_no_digit',
            )
        
        # التحقق من وجود رمز خاص
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            raise ValidationError(
                _("يجب أن تحتوي كلمة المرور على رمز خاص واحد على الأقل."),
                code='password_no_symbol',
            )
    
    def get_help_text(self):
        """
        نص المساعدة للمستخدم
        """
        return _(
            "يجب أن تتكون كلمة المرور من %(min_length)d حرف على الأقل، "
            "وتحتوي على حرف كبير، وحرف صغير، ورقم، ورمز خاص."
        ) % {'min_length': self.min_length}