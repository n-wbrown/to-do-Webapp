ENV=picarro-test

develop:
	conda create -n $(ENV) python=3.7
	conda activate $(ENV)
	conda install pip
	pip install -r requirements.txt
	pip install -e .
	echo "Use `conda activate picarro-test` to enter the development environment."

run:
	gunicorn -w 1 --bind 127.0.0.1:5000 todo:deploy_app

dev: export FLASK_APP=todo
dev: export FLASK_ENV=development
dev:
	flask run

test:
	pytest
