import os

import uvicorn
from dotenv import load_dotenv

from src.main import app

HOST = "0.0.0.0"
PORT = 8000


def run_server() -> None:
    load_dotenv()
    uvicorn.run(app, port=PORT, host=HOST)


if __name__ == "__main__":
    run_server()
