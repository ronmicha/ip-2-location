import os
import time
from collections import defaultdict
from typing import DefaultDict

from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from src.api.router import router as v1_router
from src.common.consts import (
    DEFAULT_MAX_REQUESTS_PER_SECOND,
    MAX_REQUESTS_PER_SECOND_ENV_VAR,
    RATE_LIMIT_WINDOW_SIZE,
)
from src.common.context import init_dal_instance

MAX_REQUESTS_PER_SECOND = int(
    os.getenv(MAX_REQUESTS_PER_SECOND_ENV_VAR, DEFAULT_MAX_REQUESTS_PER_SECOND)
)

request_counts: DefaultDict[str, list[float]] = defaultdict(lambda: [])

app = FastAPI()


@app.exception_handler(Exception)
async def exception_handler(request: Request, exc: Exception):
    """
    General exception handler. Catches (almost) any error and returns an expected response
    """
    return JSONResponse(status_code=500, content={"error": str(exc)})


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc: HTTPException):
    """
    FastAPI has a built-in exception handler for `HTTPException`, so this error type is not caughed in the general exception handler.
    This handler overrides the built-in handler and returns the expected error response.
    """
    return JSONResponse(status_code=exc.status_code, content={"error": exc.detail})


@app.exception_handler(RequestValidationError)
async def request_validation_exception_handler(request, exc: RequestValidationError):
    """
    FastAPI has a built-in exception handler for `RequestValidationError`, so this error type is not caughed in the general exception handler.
    This handler overrides the built-in handler and returns the expected error response.
    """
    return JSONResponse(status_code=422, content={"error": str(exc)})


@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    client_ip = request.client.host
    current_request_time = time.time()
    rate_limit_exceeded_response = _handle_request_rate_limit(
        current_request_time, client_ip
    )

    if rate_limit_exceeded_response is not None:
        return rate_limit_exceeded_response

    response = await call_next(request)
    return response


def _handle_request_rate_limit(
    current_request_time: float, client_ip: str
) -> Response | None:
    requests_so_far = request_counts[client_ip]

    if len(requests_so_far) < MAX_REQUESTS_PER_SECOND - 1:
        request_counts[client_ip].append(current_request_time)
        return

    window_start_time = requests_so_far[0]
    if current_request_time - window_start_time >= RATE_LIMIT_WINDOW_SIZE:
        request_counts[client_ip].append(current_request_time)
        request_counts[client_ip].pop(0)
        return

    headers = {"X-Retry-After": str(RATE_LIMIT_WINDOW_SIZE)}
    return JSONResponse(
        status_code=429,
        content={"error": "Too many requests"},
        headers=headers,
    )


init_dal_instance()


# Healthcheck endpoint
@app.get("/")
def healthcheck():
    return {"message": "IP2Country service is healthy!"}


app.include_router(v1_router)
