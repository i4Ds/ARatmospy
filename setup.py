from setuptools import find_packages, setup

setup(
    name="aratmospy",
    version="1.0.0",
    description="Autoregressive atmosphere generator",
    author="Srikar Srinath",
    url="https://github.com/i4Ds/ARatmospy",
    packages=find_packages(),
    install_requires=[
        "astropy",
        "matplotlib",
        "numpy",
        "pyfftw",
        "scipy>=1.9",
    ],
)
