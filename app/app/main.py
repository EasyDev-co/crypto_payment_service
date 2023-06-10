from app.api import deps
from fastapi import FastAPI, Response
from app.core.config import settings, EnvEnum
from app.core.containers import Container
from fastapi.middleware.cors import CORSMiddleware
from app.exceptions.base import (
    BaseNotFound,
    YouHaveNoRights,
    BaseUserException,
)


def create_app():
    container = Container()
    container.wire(modules=[deps])
    fastapi_app = FastAPI(
        title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json"
    )
    fastapi_app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    fastapi_app.container = container

    fastapi_app.include_router(api.api_router, prefix=settings.API_V1_STR)
    return fastapi_app


if settings.PYTHON_ENV in [EnvEnum.development, EnvEnum.production]:
    sentry_sdk.init(
        dsn=settings.SENTRY_DSN,
        traces_sample_rate=1.0,
    )


app = create_app()


@app.exception_handler(BaseNotFound)
async def custom_http_exception_handler(request, exc):
    print(exc)
    return Response(status_code=404, content=str(exc))


@app.exception_handler(YouHaveNoRights)
async def custom_http_exception_handler(request, exc):
    print(exc)
    return Response(status_code=403, content=str(exc))


@app.exception_handler(BaseUserException)
async def custom_http_exception_handler(request, exc):
    print(exc)
    return Response(status_code=400, content=str(exc))