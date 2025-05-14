import os
from typing import Dict, Optional, Union
from django.conf import settings

# Define engines with type annotation
engines: Dict[str, str] = {
    "sqlite": "django.db.backends.sqlite3",
    "postgresql": "django.db.backends.postgresql_psycopg2",
    "mysql": "django.db.backends.mysql",
}


def config() -> Dict[str, Optional[Union[str, int]]]:
    """
    Generate the database configuration dictionary based on environment variables.

    Returns:
        A dictionary containing database configuration.
    """
    service_name: str = os.getenv("DATABASE_SERVICE_NAME", "").upper().replace("-", "_")
    engine: str = engines.get(os.getenv("DATABASE_ENGINE", ""), engines["sqlite"])

    name: Optional[str] = os.getenv("DATABASE_NAME")
    if not name and engine == engines["sqlite"]:
        name = os.path.join(settings.BASE_DIR, "db.sqlite3")

    return {
        "ENGINE": engine,
        "NAME": name,
        "USER": os.getenv("DATABASE_USER"),
        "PASSWORD": os.getenv("DATABASE_PASSWORD"),
        "HOST": os.getenv(f"{service_name}_SERVICE_HOST"),
        "PORT": os.getenv(f"{service_name}_SERVICE_PORT"),
    }
