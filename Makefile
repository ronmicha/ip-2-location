setup:
	python3.10 -m venv .venv
	. .venv/bin/activate
	pip install -r requirements.txt

start:
	PYTHONPATH=. python3.10 src/run_server.py

test:
	PYTHONPATH=. pytest tests

docker_build:
	docker build -t service .

docker_run:
	docker run -p 8000:8000 --env-file .env --name ip_2_location service || docker run -p 8000:8000 --name ip_2_location service

docker_test:
	docker exec ip_2_location sh -c 'PYTHONPATH=. pytest tests'

format:
	ruff check --fix --select I