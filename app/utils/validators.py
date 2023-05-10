from django.core.exceptions import ValidationError
from django.conf import settings

def validate_img_extension(value):
    if(not value.name.endswith('.zip')):
        raise ValidationError("Only files with zip extension are allowed")
    elif(value.size > settings.MAX_UPLOAD_SIZE):
        raise ValidationError("The max size must be less than 15MB")