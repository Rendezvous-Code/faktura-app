release: python --pythonpath app manage.py migrate --no-input
web: gunicorn --pythonpath app app.wsgi --log-file -