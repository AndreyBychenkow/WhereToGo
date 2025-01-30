import os
import sys

# Укажите путь к корневой папке вашего проекта (где лежит папка WhereToGo)
sys.path.append('/home/decebell032/decebell032.pythonanywhere.com')

# Укажите переменные окружения для Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'WhereToGo.settings')
os.environ['DJANGO_SECRET_KEY'] = 'django-insecure-1wif%f1%o+qb$k%f^v-1d0)ubacaew4u(hq=btpq=z96!+wj81'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
