frontend.install:
	npm install

frontend.build: frontend.install
	npm run build

#frontend.collect_static:
	#python manage.py collectstatic --noinput

frontend: frontend.build ## Build the frontend and collect its static files



migrate: ## Apply Django migrations (and our permission/group fixtures)
	python manage.py migrate
	#python manage.py loaddata core/fixtures/*.json



deploy: frontend migrate ## Deploy the app (frontend, migrations, ...)



run.dev: deploy ## Run the app server in development mode
	python manage.py runserver
