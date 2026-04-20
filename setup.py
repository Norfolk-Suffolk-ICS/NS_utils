from setuptools import setup, find_packages

setup(
    name="NS_utils",
    version="0.1.7",
    author="Ibrahim Khan",
    description="Common Python utility functions and NS ICS styling",
    url="https://github.com/Norfolk-Suffolk-ICS/NS_utils",
    packages=find_packages(),
    install_requires=[],
    include_package_data=True,
    package_data={
        "ns_styles": ["styles/NS.mplstyle", "styles/NS_plotly.json"],
        'py_utils': ['assets/*'],
    },
)