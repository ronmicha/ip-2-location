from fastapi import FastAPI

from src.api.router import router as v1_router
from src.common.context import set_dal_instance
from src.middlewares import set_middlewares

app = FastAPI()


set_middlewares(app)
set_dal_instance()


# Healthcheck endpoint
@app.get("/")
def healthcheck():
    return {"message": "IP2Country service is healthy!"}


app.include_router(v1_router)
