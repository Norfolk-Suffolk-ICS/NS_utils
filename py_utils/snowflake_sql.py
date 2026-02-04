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

DEFAULT_TOML_PATH = os.path.join(os.path.dirname(__file__), "..", "Setup", "connections.toml")


class SnowflakeCredentialsError(Exception):
    """Raised when required Snowflake credentials are missing."""
    pass


def create_snowflake_sql_engine(
    profile_env: str = None,  # default to None (should be 'prd' or 'dev')
    toml_path: str = DEFAULT_TOML_PATH, **kwargs):
    """
    Create a Snowflake SQLAlchemy engine using connections.toml.
    profile_env: 'prd' or 'dev'

    SQL files must fully qualify objects:
    DB.SCHEMA.TABLE
    """

    if profile_env is None or profile_env.lower() not in ["prd", "dev"]:
        raise ValueError("Please input the Snowflake environment - 'prd' or 'dev'")

    # Map short name to TOML section
    profile_map = {
        "prd": "icsdatahub-prd",
        "dev": "icsdatahub-dev"
    }
    profile = profile_map[profile_env.lower()]

    if not os.path.isfile(toml_path):
        raise SnowflakeCredentialsError(f"connections.toml not found at: {toml_path}")

    config = toml.load(toml_path)

    if profile not in config:
        raise SnowflakeCredentialsError(f"Profile '{profile}' not found in {toml_path}")

    cfg = config[profile]

    required = ["account", "user", "warehouse"]
    missing = [k for k in required if not cfg.get(k)]

    if missing:
        raise SnowflakeCredentialsError(f"Missing required Snowflake fields: {missing}")

    url = URL(
        account=cfg["account"],
        user=cfg["user"],
        warehouse=cfg["warehouse"],
        role=cfg.get("role"),
        authenticator=cfg.get("authenticator", "externalbrowser"),
    )

    return create_engine(url, **kwargs)



def load_data_try_parquet_first(sql_engine, parquet_file_name: str, sql_path: str) -> pd.DataFrame:
    """
    Execute a SQL file against Snowflake and cache results to parquet.

    - Works across ANY database/schema
    - All parquet files are stored under '../Data/' by default.
    - SQL must fully qualify table names
    """

    # Ensuring dataset saved from sql file is in folder ---> 'Data'
    data_dir = os.path.abspath(os.path.join("..", "Data"))  
    os.makedirs(data_dir, exist_ok=True)                     # create folder if missing

    # Use only the filename part if parquet_file_name includes a path
    filename = os.path.basename(parquet_file_name)
    parquet_file_name = os.path.join(data_dir, filename)

    # Return cached parquet if it exists
    if os.path.isfile(parquet_file_name):
        return pd.read_parquet(parquet_file_name)

    # Ensure SQL file exists
    if not os.path.isfile(sql_path):
        raise FileNotFoundError(f"SQL file not found: {sql_path}")

    # Read SQL file
    with open(sql_path, "r") as f:
        sql_string = f.read()

    # Execute SQL
    with sql_engine.connect() as conn:
        result = conn.execute(text(sql_string))
        rows = result.fetchall()

        if not rows:
            raise ValueError("SQL script returned no results")

        df = pd.DataFrame(rows, columns=result.keys())

    df.to_parquet(parquet_file_name)

    return df