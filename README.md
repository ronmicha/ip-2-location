# IP-2-Location

## Overview

FastAPI service that gets a REST API request with
an IP address and returns its location (country, city)

### API spec

To view the service API spec:

- Run the service
- Navigate to `/docs`

### Rate limit

- The rate limit mechanism enforces that the service handles a predefined number of requests per second per client IP
- If the rate limit is exceeded per client IP, the service will block the requests and return a response with a `429` status code
- The rate limit mechanism assumes the service has only one instance

## Configuration

The service expects the following environment variables:

- `DATASTORE_TYPE` (Optional):
  - The datastore type which the service uses as a DB
  - Default: `csv`
- `MAX_REQUESTS_PER_SECOND` (Optional):
  - The maximum number of allowed requests per second. This is enforced by the rate limit mechanism
  - Default: 5

## How to run locally

If you want to override the default environment variables

1. Create a `.env` file in the repo root
1. Set the environment variables

### With Docker

1. On the first time, run: `make docker_build`
1. If you don't have a `.env` file, run: `make docker_run`
1. If you have a `.env` file, run: `make docker_run_env`

### Without Docker

1. Make sure python 3.10 is installed
1. On the first time, run: `make setup`
1. Run: `make start`

## How to run the tests

1. On the first time, run: `make setup`
1. Run: `make test`

## How to add a new datastore?

1. In the `src/dal` directory, implement a new DAL class that inherits from `BaseDAL`
1. Update the `DATASTORE_TYPE_TO_DAL` dictionary in `src/api/dependencies.py`, and map the new datastore type to the new DAL class
1. If you want to use the new datastore type, set it in the `DATASTORE_TYPE` environment variable, and run the service
