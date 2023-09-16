import os

from pydantic import BaseSettings


class Settings(BaseSettings):
    NAME: str = "governance"
    VERSION: str = "v0.5.0"  # x-release-please-version

    NETWORK_NAME: str = "mainnet"

    # Ports
    PORT: int = 8000
    HEALTH_PORT: int = 8180
    METRICS_PORT: int = 9400

    METRICS_ADDRESS: str = "localhost"

    # Prefix
    REST_PREFIX: str = "/api/v1"
    HEALTH_PREFIX: str = "/heath"
    METRICS_PREFIX: str = "/metrics"
    DOCS_PREFIX: str = "/api/v1/governance/docs"

    CORS_ALLOW_ORIGINS: str = "*"
    CORS_ALLOW_CREDENTIALS: bool = False
    CORS_ALLOW_METHODS: str = "GET,POST,HEAD,OPTIONS"
    CORS_ALLOW_HEADERS: str = ""
    CORS_EXPOSE_HEADERS: str = "x-total-count"

    # Monitoring
    HEALTH_POLLING_INTERVAL: int = 60

    # ICON Nodes
    ICON_NODE_URL: str = "https://api.icon.community/api/v3"
    BACKUP_ICON_NODE_URL: str = "https://ctz.solidwallet.io/api/v3"

    # API endpoints
    COMMUNITY_API_ENDPOINT: str = "https://tracker.icon.community"

    # Logs service - For getting value for iscore
    # TODO: Replace this when stateful processing comes in maybe
    LOGS_SERVICE_URL: str = "https://tracker.icon.community"

    # ICON Peers - Used to discover nodes across the network
    PEER_SEED_IP: str = "52.196.159.184"
    PEER_SEED_ADDRESS: str = "hx9c63f73d3c564a54d0eed84f90718b1ebed16f09"

    # Kafka
    KAFKA_BROKER_URL: str = "localhost:29092"
    SCHEMA_REGISTRY_URL: str = "http://localhost:8081"
    CONSUMER_IS_TAIL: bool = False

    # Topics
    CONSUMER_GROUP: str = "governance"
    CONSUMER_TOPIC_BLOCKS: str = "blocks"
    # Backfilling
    CONSUMER_AUTO_OFFSET_RESET: str = "earliest"
    JOB_ID: str = None

    # DB
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "changeme"
    POSTGRES_SERVER: str = "127.0.0.1"
    POSTGRES_PORT: str = "5432"
    POSTGRES_DATABASE: str = "postgres"

    # Endpoints
    MAX_PAGE_SIZE: int = 100

    governance_address: str = "cx0000000000000000000000000000000000000000"
    CRON_SLEEP_SEC: int = 600

    class Config:
        case_sensitive = True


if os.environ.get("ENV_FILE", False):
    settings = Settings(_env_file=os.environ.get("ENV_FILE"))
else:
    settings = Settings()
