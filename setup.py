from setuptools import setup, find_packages

setup(
    name="NS_utils",
    version="0.1.8",
    author="Ibrahim Khan",
    description="Common Python utility functions and NS ICS styling",
    url="https://github.com/Norfolk-Suffolk-ICS/NS_utils",
    packages=find_packages(),
    install_requires=[
        "pandas",
        "polars",
        "pyarrow",                                          # parquet caching in load_data_try_parquet_first
        "SQLAlchemy<2.1",                                   # snowflake-sqlalchemy breaks on 2.1
        "snowflake-sqlalchemy",                             # Snowflake connection
        "snowflake-connector-python[secure-local-storage]", # Snowflake driver + SSO login caching
        "toml",                                             # reads connections.toml
        "matplotlib",                                       # ns_styles
        "plotly",                                           # ns_styles
        "nbconvert",                                        # HTML / slide export
        "nbformat",                                         # HTML / slide export
    ],
    include_package_data=True,
    package_data={
        "ns_styles": ["styles/NS.mplstyle", "styles/NS_plotly.json"],
        'py_utils': ['assets/*'],
    },
)