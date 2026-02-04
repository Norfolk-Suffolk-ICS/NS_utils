from setuptools import setup, find_packages

setup(
    name="SNEE_utils",
    version="0.1.0",
    packages=find_packages(),  # This will find both py_utils and style_utils
    description="Common Python utility functions and SNEE stylings to reuse across projects.",
    author="Ibrahim Khan",
    license="Apache-2.0",
    license_files=["LICENSE"],  # correct field name
    install_requires=[
        "pandas>=2.3.0",
        "numpy>=2.0.0",
        "sqlalchemy>=2.0.0",
        "snowflake-connector-python>=4.2.0",
        "toml>=0.10.2",
        "pyarrow>=9.0.0"
        # Add other dependencies from your requirements.txt as needed
    ],
    include_package_data=True,  # include non-code files via MANIFEST.in
    package_data={
        "snee_styles": ["styles/SNEE.mplstyle", "styles/SNEE_plotly.json"],
        # py_utils usually does not need package_data unless you have non-code files
    },
    python_requires=">=3.8",  # optional: enforce minimum Python version
)