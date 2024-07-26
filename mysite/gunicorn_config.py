command = '/var/www/blog/env/bin/gunicorn'
python_path = '/var/www/blog/mysite'
bind = '127.0.0.1:8001'
workers = 5
user = 'www'
raw_env = 'DJANGO_SETTINGS_MODULE=mysite.settings'