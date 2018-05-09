"""Setup file for the Dummy-Module package.

   Adapted from the Python Packaging Authority template.
"""

from setuptools import setup, find_packages  # Always prefer setuptools
from codecs import open  # To use a consistent encoding
from os import path, walk
import sys, warnings, importlib, re

MAJOR = 0
MINOR = 0
MICRO = 1
ISRELEASED = False
VERSION = '%d.%d.%d' % (MAJOR, MINOR, MICRO)
QUALIFIER = ''

DISTNAME = 'oggmcontrib'
LICENSE = 'GPLv3+'
AUTHOR = 'OGGM Developers'
AUTHOR_EMAIL = 'some.contributor@contribute.oggm'
URL = 'http://oggm.org'
CLASSIFIERS = [
        # How mature is this project? Common values are
        # 3 - Alpha  4 - Beta  5 - Production/Stable
        'Development Status :: 3 - Alpha',
        # Indicate who your project is intended for
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU General Public License ' +
        'v3 or later (GPLv3+)',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ]

DESCRIPTION = 'Open Global Glacier Model - example external package'
LONG_DESCRIPTION = """This repository shows how you can develop
an external package for OGGM and keep control over it without having to 
put your code on the main repository.

Links
-----
- Project website: http://oggm.org
- HTML documentation: http://oggm.readthedocs.io
- Source code: http://github.com/oggm/oggm
"""

# code to extract and write the version copied from pandas
FULLVERSION = VERSION
write_version = True

if not ISRELEASED:
    import subprocess
    FULLVERSION += '.dev'

    pipe = None
    for cmd in ['git', 'git.cmd']:
        try:
            pipe = subprocess.Popen(
                [cmd, "describe", "--always", "--match", "v[0-9]*"],
                stdout=subprocess.PIPE)
            (so, serr) = pipe.communicate()
            if pipe.returncode == 0:
                break
        except:
            pass

    if pipe is None or pipe.returncode != 0:
        # no git, or not in git dir
        if path.exists('oggmcontrib/version.py'):
            warnings.warn("WARNING: Couldn't get git revision, using existing "
                          "oggmcontrib/version.py")
            write_version = False
        else:
            warnings.warn("WARNING: Couldn't get git revision, using generic "
                          "version string")
    else:
        # have git, in git dir, but may have used a shallow clone (travis)
        rev = so.strip()
        # makes distutils blow up on Python 2.7
        if sys.version_info[0] >= 3:
            rev = rev.decode('ascii')

        if not rev.startswith('v') and re.match("[a-zA-Z0-9]{7,9}", rev):
            # partial clone, manually construct version string
            # this is the format before we started using git-describe
            # to get an ordering on dev version strings.
            rev = "v%s.dev-%s" % (VERSION, rev)

        # Strip leading v from tags format "vx.y.z" to get th version string
        FULLVERSION = rev.lstrip('v').replace(VERSION + '-', VERSION + '+')
else:
    FULLVERSION += QUALIFIER


def write_version_py(filename=None):
    cnt = """\
version = '%s'
short_version = '%s'
isreleased = %s
"""
    if not filename:
        filename = path.join(path.dirname(__file__), 'oggmcontrib',
                             'version.py')

    a = open(filename, 'w')
    try:
        a.write(cnt % (FULLVERSION, VERSION, ISRELEASED))
    finally:
        a.close()


if write_version:
    write_version_py()


def check_dependencies(package_names):
    """Check if packages can be imported, if not throw a message."""
    not_met = []
    for n in package_names:
        try:
            _ = importlib.import_module(n)
        except ImportError:
            not_met.append(n)
    if len(not_met) != 0:
        errmsg = "Warning: the following packages could not be found: "
        print(errmsg + ', '.join(not_met))


req_packages = ['numpy',
                'scipy',
                ]
check_dependencies(req_packages)


def file_walk(top, remove=''):
    """
    Returns a generator of files from the top of the tree, removing
    the given prefix from the root/file result.
    """
    top = top.replace('/', path.sep)
    remove = remove.replace('/', path.sep)
    for root, dirs, files in walk(top):
        for file in files:
            yield path.join(root, file).replace(remove, '')


setup(
    # Project info
    name=DISTNAME,
    version=FULLVERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    # The project's main homepage.
    url=URL,
    # Author details
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    # License
    license=LICENSE,
    classifiers=CLASSIFIERS,
    # What does your project relate to?
    keywords=['geosciences', 'glaciers', 'climate', 'gis'],
    # We are a python 3 only shop
    python_requires='>=3.4',
    # Find packages automatically
    packages=find_packages(exclude=['docs']),
    # Decided not to let pip install the dependencies, this is too brutal
    install_requires=[],
    # additional groups of dependencies here (e.g. development dependencies).
    extras_require={},
    # data files that need to be installed
    package_data={},
    # Old
    data_files=[],
    # Executable scripts
    entry_points={},
)
