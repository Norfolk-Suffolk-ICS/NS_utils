from setuptools import setup, find_packages

setup(
    name="SNEE_utils",
    version="0.1.0",
    packages=find_packages(),  # This will find both py_utils and style_utils
    description="Common Python utility functions and SNEE stylings to reuse across projects.",
    author="Ibrahim Khan",
    license="Apache-2.0",
    license_files=["LICENSE"],  # correct field name
    install_requires=[],
    include_package_data=True,  # include non-code files via MANIFEST.in
    package_data={
        "snee_styles": ["styles/SNEE.mplstyle", "styles/SNEE_plotly.json"],
        # py_utils usually does not need package_data unless you have non-code files
    },
)