web: gunicorn xbeta.wsgi
web: python xbeta/manage.py collectstatic --noinput; bin/gunicorn_django --workers=4 --bind=0.0.0.0:$PORT xbeta/settings.py