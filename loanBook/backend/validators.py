from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

class CustomPasswordValidator:
    def validate(self, password, user=None):
        if not any(char.isdigit() for char in password):
            raise ValidationError(_('Le mot de passe doit contenir au moins un chiffre.'), code='password_no_number')
        if not any(char.isalpha() for char in password):
            raise ValidationError(_('Le mot de passe doit contenir au moins une lettre.'), code='password_no_letter')
        if not any(char.islower() for char in password):
            raise ValidationError(_('Le mot de passe doit contenir au moins une minuscule.'), code='password_no_lower')
        if not any(char.isupper() for char in password):
            raise ValidationError(_('Le mot de passe doit contenir au moins une majuscule.'), code='password_no_upper')
        if not any(char in "!@#$%^&*()_+" for char in password):
            raise ValidationError(_('Le mot de passe doit contenir au moins un symbole (!@#$%^&*()_+).'), code='password_no_symbol')

    def get_help_text(self):
        return _("Votre mot de passe doit contenir au moins un chiffre, une lettre, une minuscule, une majuscule et un symbole (!@#$%^&*()_+).")
