#!/usr/bin/env python
import sys
import os.path
import os
import platform
import warnings
import couchbase_version

try:
    if os.environ.get('PYCBC_NO_DISTRIBUTE'):
        raise ImportError()

    from setuptools import setup, Extension
except ImportError:
    from distutils.core import setup, Extension

extoptions = {}
pkgdata = {}
pkgversion = None

try:
    couchbase_version.gen_version()
except couchbase_version.CantInvokeGit:
    pass

pkgversion = couchbase_version.get_version()


LCB_NAME = None
if sys.platform != 'win32':
    extoptions['libraries'] = ['couchbase']
else:
    warnings.warn("I'm detecting you're running windows."
                  "You might want to modify "
                  "the 'setup.py' script to use appropriate paths")


    # The layout i have here is an ..\lcb-winbuild, in which there are subdirs
    # called 'x86' and 'x64', for x86 and x64 architectures. The default
    # 'nmake install' on libcouchbase will install them to 'deps'
    bit_type = platform.architecture()[0]
    lcb_root = os.path.join(os.path.pardir, 'lcb-winbuild')

    if bit_type.startswith('32'):
        lcb_root = os.path.join(lcb_root, 'x86')
    else:
        lcb_root = os.path.join(lcb_root, 'x64')

    lcb_root = os.path.join(lcb_root, 'deps')

    extoptions['libraries'] = ['libcouchbase']
    ## Enable these lines for debug builds
    #extoptions['extra_compile_args'] = ['/Zi']
    #extoptions['extra_link_args'] = ['/DEBUG']
    extoptions['library_dirs'] = [os.path.join(lcb_root, 'lib')]
    extoptions['include_dirs'] = [os.path.join(lcb_root, 'include')]
    pkgdata['couchbase'] = ['libcouchbase.dll']


SOURCEMODS = (
        'argument',
        'exceptions',
        'ext',
        'result',
        'opresult',
        'callbacks',
        'convert',
        'connection',
        'store',
        'constants',
        'multiresult',
        'miscops',
        'typeutil',
        'oputil',
        'get',
        'arithmetic',
        'http',
        'htresult',
        'ctranscoder',
        'observe',
        os.path.join('viewrow', 'viewrow'),
        os.path.join('contrib', 'jsonsl', 'jsonsl')
        )

extoptions['sources'] = [ os.path.join("src", m + ".c") for m in SOURCEMODS ]
module = Extension('couchbase._libcouchbase', **extoptions)

setup(
    name = 'couchbase',
    version = pkgversion,
    url="https://github.com/couchbase/couchbase-python-client",
    author="Couchbase, Inc.",
    author_email="mark.nunberg@couchbase.com",
    license="Apache License 2.0",
    description="Python Client for Couchbase",
    long_description=open("README.rst", "r").read(),
    keywords=["couchbase", "nosql", "pycouchbase", "libcouchbase"],

    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: Apache Software License",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: Implementation :: CPython",
        "Topic :: Database",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules"],

    ext_modules = [module],
    packages = ['couchbase', 'couchbase.views'],
    package_data = pkgdata
)
