def init_django():
    import os
    import django
    from django.conf import settings

    if settings.configured:
        return

    settings.configure(
        INSTALLED_APPS=[
            'api',
        ],
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': 'db.sqlite3',
            }
        },
        DEFAULT_AUTO_FIELD = 'django.db.models.AutoField',
        TIME_ZONE = 'America/Sao_Paulo',
        USE_TZ = True
    )
    django.setup()