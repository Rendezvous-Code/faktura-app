release: python --pythonpath app manage.py migrate
web: gunicorn --pythonpath app app.wsgi --log-file -