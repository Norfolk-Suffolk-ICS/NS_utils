from setuptools import setup, find_packages

setup(
    name="NS_utils",
    version="0.1.0",
    packages=find_packages(),  # This will find both py_utils and style_utils
    description="Common Python utility functions and NS stylings to reuse across projects.",
    author="Ibrahim Khan",
    license="Apache-2.0",
    license_files=["LICENSE"],  # correct field name
    install_requires=[],
    include_package_data=True,  # include non-code files via MANIFEST.in
    package_data={
        "ns_styles": ["styles/NS.mplstyle", "styles/NS_plotly.json"],
        # py_utils usually does not need package_data unless you have non-code files
    }, 
)