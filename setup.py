from setuptools import setup, find_packages
from os import path

directory = path.abspath(path.dirname(__file__))
requirements = open(
    path.join(directory, 'requirements.txt')
).read().splitlines()


setup(
    name="todo",
    author="Nolan Brown",
    python_requires='>=3.7',
    entry_points={
        'console_scripts': [
            'todo = todo.bin:main',
        ]
    },
    packages=find_packages()
)

