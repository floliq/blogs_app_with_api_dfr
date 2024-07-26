#!/bin/bash
source /var/www/blog/env/bin/activate
exec gunicorn -c "/var/www/blog/mysite/gunicorn_config.py" mysite.wsgi