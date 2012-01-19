import os

cur_file = os.path.abspath(__file__)
django_base = os.path.join(os.path.dirname(cur_file), '..')
db_file = os.path.join(django_base, 'nextmon.sqlite')

DATABASES = {
    'default' : {
        'ENGINE' : 'django.db.backends.sqlite3',
        'NAME' : db_file,
    },
}

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'e_8xq=+r)nh=!tvvw19x9j*slkafcded5_=bhaaecrwmwvmhz3%'

DEBUG = True
