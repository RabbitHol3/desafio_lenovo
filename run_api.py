import logging, time, os, django, sys
from django.core.wsgi import get_wsgi_application 
from django.core.management import call_command
from multiprocessing import Process

def init_api():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'desafio_lenovo.settings')
    application = get_wsgi_application()
    call_command('makemigrations')
    call_command('migrate')    
    call_command(command_name='runserver')
    
def main():
    print('Starting API')
    Process(target=init_api).start()    
    print('API is running...')
    
if __name__ == '__main__':
    main()