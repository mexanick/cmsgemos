import os
#import sys
#BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#sys.path.append(BASE_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gempython.utils.db.settings.local")
SECRET_KEY = 'ef7$_)r0$#(x)ovd^m_6_bevsonkaxalvrhds9@ilb_p0o&-xn'

INSTALLED_APPS = [
    'gempython.utils.db.ldqm_db',
    ]
DATABASES = {
    'default': {
        'ENGINE':   'django.db.backends.mysql',
        'NAME':     'ldqm_db',
        'PORT':     3306,
        'HOST':     'gemvm-daqcc7.cms',
        'USER':     'ldqm_dbuser',
        'PASSWORD': 'clod4_Callow',
    }
    #'default': {
    #    'ENGINE': 'django.db.backends.sqlite3',
    #    'NAME': os.path.join(os.getenv('BUILD_HOME'), 'ldqm-browser/LightDQM/LightDQM/lightdqm_db.sqlite3'),
    #}
}
