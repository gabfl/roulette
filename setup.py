from setuptools import setup

try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
except(IOError, ImportError):
    long_description = open('README.md').read()

setup(
    name='roulette',
    version='1.5',
    description='Roullette game',
    long_description=long_description,
    author='Gabriel Bordeaux',
    author_email='pypi@gab.lc',
    url='https://github.com/gabfl/roulette',
    license='MIT',
    packages=['roulette', 'roulette.utils', 'roulette.vars'],
    package_dir={'roulette': 'src'},
    install_requires=['argparse', 'configparser',
                      'tabulate'],  # external dependencies
    entry_points={
        'console_scripts': [
            'roulette = roulette.play:main',
        ],
    },
    classifiers=[  # see https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Topic :: Games/Entertainment :: Simulation',
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS',
        'Operating System :: POSIX :: Linux',
        'Natural Language :: English',
        #  'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python',
        'Development Status :: 4 - Beta',
        #  'Development Status :: 5 - Production/Stable',
    ],
)
