import os
import toml
import pandas as pd

from sqlalchemy import create_engine, text
from snowflake.sqlalchemy import URL

__all__ = [
    "SnowflakeCredentialsError",
    "create_snowflake_sql_engine",
    "load_data_try_parquet_first",
]

DEFAULT_TOML_PATH = "connections.toml"
DEFAULT_PROFILE = "icsdatahub-prd"


class SnowflakeCredentialsError(Exception):
    """
    Raised when required Snowflake credentials are missing.
    """
    pass


def create_snowflake_sql_engine(
    profile: str = DEFAULT_PROFILE,
    toml_path: str = DEFAULT_TOML_PATH,
    **kwargs,
):
    """
    Create a Snowflake SQLAlchemy engine using connections.toml.

    NOTE:
    - No database
    - No schema

    SQL files must fully qualify objects:
    DB.SCHEMA.TABLE
    """

    if not os.path.isfile(toml_path):
        raise SnowflakeCredentialsError(
            f"connections.toml not found at: {toml_path}"
        )

    config = toml.load(toml_path)

    if profile not in config:
        raise SnowflakeCredentialsError(
            f"Profile '{profile}' not found in {toml_path}"
        )

    cfg = config[profile]

    required = ["account", "user", "warehouse"]
    missing = [k for k in required if not cfg.get(k)]

    if missing:
        raise SnowflakeCredentialsError(
            f"Missing required Snowflake fields: {missing}"
        )

    url = URL(
        account=cfg["account"],
        user=cfg["user"],
        warehouse=cfg["warehouse"],
        role=cfg.get("role"),
        authenticator=cfg.get("authenticator", "externalbrowser"),
    )

    return create_engine(url, **kwargs)


def load_data_try_parquet_first(
    sql_engine,
    parquet_path: str,
    sql_path: str,
) -> pd.DataFrame:
    """
    Execute a SQL file against Snowflake and cache results to parquet.

    - Works across ANY database/schema
    - SQL must fully qualify table names
    """

    if os.path.isfile(parquet_path):
        return pd.read_parquet(parquet_path)

    if not os.path.isfile(sql_path):
        raise FileNotFoundError(f"SQL file not found: {sql_path}")

    with open(sql_path, "r") as f:
        sql_string = f.read()

    with sql_engine.connect() as conn:
        result = conn.execute(text(sql_string))
        rows = result.fetchall()

        if not rows:
            raise ValueError("SQL script returned no results")

        df = pd.DataFrame(rows, columns=result.keys())

    df.to_parquet(parquet_path)
    return df
