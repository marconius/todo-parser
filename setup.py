from setuptools import find_packages, setup

setup(
    name='todo parser',
    packages=find_packages(),
    entry_points={'console_scripts': [
        'todo-parser = todo_parser.__main__:cli',
    ]},
)
