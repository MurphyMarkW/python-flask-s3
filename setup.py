from setuptools import setup

setup(
    name='flasks3',
    packages=[
        'flasks3',
        'flasks3.auth',
        'flasks3.drivers',
    ],
    install_requires = [
        'flask>=0.10.1',
    ],
)
