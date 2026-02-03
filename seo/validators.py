
import re
from django.core.exceptions import ValidationError

def validate_seo_slug(value):
    if not re.match(r'^[a-z0-9\-]+$', value):
        raise ValidationError(
            'Slugs can only contain lowercase letters, numbers, and hyphens'
        )
    if value.startswith('-') or value.endswith('-'):
        raise ValidationError(
            'Slugs cannot start or end with a hyphen'
        )