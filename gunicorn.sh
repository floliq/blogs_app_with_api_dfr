#!/bin/bash
source /var/www/blogs_app_with_api_dfr/env/bin/activate
exec gunicorn -c "/var/www/blogs_app_with_api_dfr/mysite/gunicorn_config.py" mysite.wsgi
