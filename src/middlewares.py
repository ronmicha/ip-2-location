import os
import time
from collections import defaultdict
from typing import DefaultDict

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from src.common.consts import (
    DEFAULT_MAX_REQUESTS_PER_SECOND,
    MAX_REQUESTS_PER_SECOND_ENV_VAR,
)

max_requests_per_second = int(
    os.getenv(MAX_REQUESTS_PER_SECOND_ENV_VAR, DEFAULT_MAX_REQUESTS_PER_SECOND)
)

request_counts: DefaultDict[str, tuple[int, float]] = defaultdict(
    lambda: (0, time.time())
)


def set_middlewares(app: FastAPI) -> None:
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
    async def request_validation_exception_handler(
        request, exc: RequestValidationError
    ):
        """
        FastAPI has a built-in exception handler for `RequestValidationError`, so this error type is not caughed in the general exception handler.
        This handler overrides the built-in handler and returns the expected error response.
        """
        return JSONResponse(status_code=422, content={"error": str(exc)})

    @app.middleware("http")
    async def rate_limit_middleware(request: Request, call_next):
        """
        Enforce rate limit for this service, according the following logic:

        Keep an in-memory dictionary that maps a client IP to its first request within the rate limit time window, and the number of requests so far.
        If the request interval is within the time window (1 second):
            If the current request count exceeds the rate limit:
                Return a 429 response with a `X-Retry-After` header.
            Else:
                Increment the client's request count.
        Else
            Reset the client's rate limit.
        """
        client_ip = request.client.host
        requests_so_far, start_time = request_counts[client_ip]
        current_request_count = requests_so_far + 1
        current_time = time.time()

        if current_time - start_time < 1:
            if current_request_count >= max_requests_per_second:
                retry_after = 1 - (current_time - start_time)
                headers = {"X-Retry-After": str(retry_after)}
                return JSONResponse(
                    status_code=429,
                    content={"error": "Too many requests"},
                    headers=headers,
                )
            else:
                request_counts[client_ip] = (current_request_count, start_time)
        else:
            request_counts[client_ip] = (1, current_time)

        response = await call_next(request)
        return response
