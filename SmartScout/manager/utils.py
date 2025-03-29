from django.core.exceptions import ValidationError

def validate_non_empty_list(value):
    if not isinstance(value, list) or len(value) < 1:
        raise ValidationError("The skills_required field must contain at least one skill.")
