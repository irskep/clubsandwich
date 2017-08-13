from setuptools import setup, find_packages


def readme():
    with open('Readme.rst') as f:
        return f.read()


setup(
    name='clubsandwich',
    version='0.1.3',
    author='Steve Johnson',
    author_email='steve@steveasleep.com',
    description="A roguelike framework",
    long_description=readme(),
    license='MIT',
    keywords=['bearlibterminal', 'roguelike'],
    include_package_data=True,
    packages=find_packages(exclude=["docs", "examples"]),
    url='http://steveasleep.com/clubsandwich',
    install_requires=[
        'bearlibterminal>=0.15',
    ],
    entry_points='''
        [console_scripts]
        babysit=clubsandwich.babysit:cli
        ''',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)
