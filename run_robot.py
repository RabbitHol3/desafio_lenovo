import time, os, django, sys
from django.core.wsgi import get_wsgi_application 
from django.core.management import call_command
from multiprocessing import Process
from robo.main import Robot

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



def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'desafio_lenovo.settings')
    
    print('Starting Automation')
    try:
        Robot(robot_name='lenovo').start()
    except Exception as e:
        print('There was an error: {}'.format(e))        
    
    print('Automation stopped')
    
if __name__ == '__main__':
    main()