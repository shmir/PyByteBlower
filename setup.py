#!/usr/bin/env python
# encoding: utf-8

from __future__ import print_function
from setuptools import setup
import io

import byteblower


def read(*filenames, **kwargs):
    encoding = kwargs.get('encoding', 'utf-8')
    sep = kwargs.get('sep', '\n')
    buf = []
    for filename in filenames:
        with io.open(filename, encoding=encoding) as f:
            buf.append(f.read())
    return sep.join(buf)


with open('requirements.txt') as f:
    required = f.read().splitlines()
install_requires = [r for r in required if r and r[0] != '#' and not r.startswith('git')]

long_description = read('README.md')


setup(
    name='pybyteblower',
    version=byteblower.__version__,
    url='https://github.com/shmir/PyByteBlower/',
    license='Apache Software License',
    author='Yoram Shamir',
    install_requires=install_requires,
    tests_require=['pytest'],
    author_email='yoram@ignissoft.com',
    description='Pip installable package wrapping ByteBlower traffic generator Python API',
    long_description=long_description,
    packages=['byteblower', 'byteblower.byteblowerll'],
    include_package_data=True,
    platforms='nt',
    test_suite='test',
    classifiers=[
        'Programming Language :: Python',
        'Development Status :: 4 - Beta',
        'Natural Language :: English',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Testing :: Traffic Generation'],
    keywords='byteblower l2l3 test tool automation',
)
