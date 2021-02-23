from setuptools import setup

setup(
    name='ARBKit',
    version='0.1',
    py_modules=['ARBKit'],
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        ARBKit=ARBKit:cli
    ''',
)