from django.core.exceptions import ValidationError


def mobile_validator(value):
    if len(value) != 11:
        raise ValidationError('شماره موبایل باید 11 رقم باشد!')

    if not str(value).startswith('09'):
        raise ValidationError('شماره موبایل با 09 شروع شود!')

    if not str(value).isdigit():
        raise ValidationError('نمیتوان در شماره موبایل از حروف استفاده کرد!')
