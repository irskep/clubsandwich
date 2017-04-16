from setuptools import setup, find_packages

setup(
    name='clubsandwich',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'appdirs',
        'bearlibterminal',
    ],
    entry_points='''
        [console_scripts]
        babysit=clubsandwich.babysit:cli
    ''',
)
