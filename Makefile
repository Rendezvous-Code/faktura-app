migrate: ## Apply Django migrations (and our permission/group fixtures)
	python manage.py migrate
	#python manage.py loaddata core/fixtures/*.json



deploy: migrate ## Deploy the app (frontend, migrations, ...)



run.dev: deploy ## Run the app server in development mode
	python manage.py runserver
