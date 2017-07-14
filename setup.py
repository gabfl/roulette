from setuptools import setup

try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
except(IOError, ImportError):
    long_description = open('README.md').read()

setup(
    name='roulette',
    version='1.2',
    description='Roullette game',
    long_description=long_description,
    author='Gabriel Bordeaux',
    author_email='pypi@gab.lc',
    url='https://github.com/gabfl/roulette',
    license='MIT',
    packages=['roulette', 'roulette.utils', 'roulette.vars'],
    package_dir={'roulette': 'src'},
    install_requires=['argparse', 'configparser', 'tabulate'],  # external dependencies
    entry_points={
        'console_scripts': [
            'roulette = roulette.play:main',
        ],
    },
)
