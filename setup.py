import pkg_resources, os, pkgutil
from setuptools import setup, find_packages
import biobox

def dependencies():
    file_ = pkg_resources.resource_filename(__name__, os.path.join('requirements', 'default.txt'))
    with open(file_, 'r') as f:
        return f.read().splitlines()


setup(
    name                 = 'biobox-py',
    version              = biobox.__version__,
    description          = 'Create and run biobox Docker containers',
    author               = 'bioboxes',
    author_email         = 'mail@bioboxes.org',
    url                  = 'http://bioboxes.org',
    install_requires     = dependencies(),

    packages             = find_packages(),
    include_package_data = True,

    classifiers = [
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'Intended Audience :: Science/Research',
        'Operating System :: POSIX'
    ],
)
