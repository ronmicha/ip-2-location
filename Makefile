setup:
	python3.10 -m venv .venv
	. .venv/bin/activate
	pip install -r requirements.txt

start:
	PYTHONPATH=. python3.10 src/run_server.py

docker_build:
	docker build -t service .

docker_run:
	docker run -p 8000:8000 service

docker_run_env:
	docker run -p 8000:8000 --env-file .env service

test:
	PYTHONPATH=. pytest tests

format:
	ruff check --fix --select I