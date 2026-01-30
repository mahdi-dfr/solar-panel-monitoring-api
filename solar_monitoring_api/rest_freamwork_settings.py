import datetime


def build_django_rest_framework(your_settings=None):
    REST_FRAMEWORK = {
        'DEFAULT_AUTHENTICATION_CLASSES': (
            'rest_framework_simplejwt.authentication.JWTAuthentication',
        ),
        'DEFAULT_PERMISSION_CLASSES': [
            'rest_framework.permissions.IsAuthenticated',
        ],
        # 'ACCESS_TOKEN_LIFETIME': datetime.timedelta(
        #     days=int(os.getenv('ACCESS_TOKEN_DAYS', '10')),
        #     minutes=int(os.getenv('ACCESS_TOKEN_MINUTES', '60')),
        #     seconds=int(os.getenv('ACCESS_TOKEN_SECONDS', '0')),
        # ),
        # 'REFRESH_TOKEN_LIFETIME': datetime.timedelta(
        #     days=int(os.getenv('REFRESH_TOKEN_DAYS', '12')),
        # ),
        # 'DEFAULT_PAGINATION_CLASS': 'solarapi.custom_drf.CustomPagination',
        # 'PAGE_SIZE': 50,
        # 'DEFAULT_FILTER_BACKENDS': [
        #     'django_filters.rest_framework.DjangoFilterBackend',
        #     'rest_framework.filters.OrderingFilter'
        # ],
        # 'DEFAULT_PARSER_CLASSES': [
        #     'solarapi.custom_drf.CustomJsonParser',
        #     'solarapi.custom_drf.CustomFormParser',
        #     'solarapi.custom_drf.CustomMultiPartParser',
        # ],
        'TEST_REQUEST_DEFAULT_FORMAT': 'json',
        # 'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    }
    if your_settings:
        REST_FRAMEWORK.update(your_settings)

    return REST_FRAMEWORK
