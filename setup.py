from setuptools import setup
from setuptools import find_packages

setup(
    name='Codeforces_CLI',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'click', 
        'requests',
        'tabulate',
        'colorama',
        'robobrowser',
        'python-dotenv',
        'lxml'
    ],
     entry_points={
        'console_scripts': [
            'cf = app.script:cli',
        ],
    },
)
