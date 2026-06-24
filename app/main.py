from fastapi import FastAPI
from app.core.config import settings
from app.api.v1 import api_router

app = FastAPI(title=settings.PROJECT_NAME)

from app.db.base import Base
from app.db.session import engine
from app.models import asset as _asset  # noqa: F401

Base.metadata.create_all(bind=engine)

app.include_router(api_router, prefix=settings.API_V1_STR)

from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from app.core.exceptions import (
    http_exception_handler,
    validation_exception_handler,
    general_exception_handler,
)

app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)


@app.get("/")
def read_root():
    return {"message": "Welcome"}
