from setuptools import setup, find_packages
import biobox

setup(
    name                 = 'biobox',
    version              = biobox.__version__,
    description          = 'Create and run biobox Docker containers',
    author               = 'bioboxes',
    author_email         = 'mail@bioboxes.org',
    url                  = 'http://bioboxes.org',
    install_requires     = open('requirements/default.txt').read().splitlines(),

    packages             = find_packages(),
    include_package_data = True,

    classifiers = [
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'Intended Audience :: Science/Research',
        'Operating System :: POSIX'
    ],
)
