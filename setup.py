from setuptools import setup, find_packages

setup(
    name="NS_utils",
    version="0.1.5",
    author="Ibrahim Khan",
    description="Common Python utility functions and NS ICS styling",
    url="https://github.com/Norfolk-Suffolk-ICS/NS_utils",
    packages=find_packages(),
    install_requires=[
        # Data access & database (Snowflake) connectivity
        "pyodbc>=5.1.0",
        "pandas>=2.3.3",
        "polars>=0.20.19",
        "openpyxl>=3.1.5",
        "toml>=0.10.2",
        "tomlkit>=0.14.0",
        "snowflake>=1.11.0",
        "snowflake-connector-python>=2.0",
        "snowflake-sqlalchemy>=1.8.2",
        "snowflake._legacy>=1.0.2",
        "snowflake.core>=1.11.0",
        "SQLAlchemy>=2.0.46",
        "sqlglot>=23.0.5",
        # Data manipulation
        "numpy>=2.0.1",
        # Visualization and plots
        "matplotlib>=3.9.2",
        "contourpy>=1.2.1",    # Often used with matplotlib for contour plots
        "cycler>=0.12.1",      # Used in matplotlib to manage property cycles (like color or line style sequences) for plots
        "seaborn>=0.13.2",
        "plotly>=5.0",
        # Notebook manipulations
        "nbconvert>=7.16.4",
        "nbformat>=5.10.4",
        "nbclient>=0.10.0",
    ],
    package_data={
        "ns_styles": ["styles/NS.mplstyle", "styles/NS_plotly.json"],
    },
)