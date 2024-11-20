from multiprocessing.pool import ThreadPool

import uvicorn
from brotli_asgi import BrotliMiddleware
from fastapi import FastAPI
from fastapi_health import health
from prometheus_client import start_http_server
from starlette.middleware.cors import CORSMiddleware

from icon_governance.api.health import is_database_online
from icon_governance.api.v1.router import api_router
from icon_governance.config import settings
from icon_governance.log import logger

app = FastAPI()

tags_metadata = [
    {
        "name": "icon-governance",
        "description": "Governance backend.",
    },
]

app = FastAPI(
    title="ICON Governance Service",
    description="...",
    version=settings.VERSION,
    openapi_tags=tags_metadata,
    openapi_url=f"{settings.DOCS_PREFIX}/openapi.json",
    docs_url=f"{settings.DOCS_PREFIX}",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin.strip() for origin in settings.CORS_ALLOW_ORIGINS.split(",")],
    allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
    allow_methods=[method.strip() for method in settings.CORS_ALLOW_METHODS.split(",")],
    allow_headers=[header.strip() for header in settings.CORS_ALLOW_HEADERS.split(",")],
    expose_headers=[header.strip() for header in settings.CORS_EXPOSE_HEADERS.split(",")],
)

app.add_middleware(
    BrotliMiddleware,
    quality=8,
)

logger.info("Starting metrics server.")
metrics_pool = ThreadPool(1)
metrics_pool.apply_async(start_http_server, (settings.METRICS_PORT, settings.METRICS_ADDRESS))
# start_http_server(9401, "localhost")

logger.info("Starting application...")
app.include_router(api_router, prefix=settings.REST_PREFIX)
app.add_api_route(settings.HEALTH_PREFIX, health([is_database_online]))

if __name__ == "__main__":
    uvicorn.run(
        "main_api:app",
        host="0.0.0.0",
        port=settings.PORT,
        log_level="info",
        workers=1,
    )
