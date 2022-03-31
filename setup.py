from setuptools import setup, find_packages

setup(
    name='ARatmospy',
    version='1.0.0',
    description='Autoregressive atmosphere generator',
    author='Srikar Srinath',
    url='https://github.com/SimonP2207/ARatmospy',
    packages=find_packages(),
    install_requires=[
        'astropy',
        'matplotlib',
        'numpy',
        'pyfftw',
        'scipy',
    ],
)
