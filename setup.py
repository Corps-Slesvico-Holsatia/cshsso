#! /usr/bin/env python3
"""Install script."""

from setuptools import setup


setup(
    name='cshsso',
    use_scm_version={
        "local_scheme": "node-and-timestamp"
    },
    setup_requires=['setuptools_scm'],
    install_requires=[
        'argon2_cffi',
        'emaillib',
        'flask',
        'peewee',
        'peeweeplus',
        'recaptcha',
        'setuptools',
        'werkzeug',
        'wsgilib'
    ],
    author='Corps Slesvico-Holsatia',
    author_email='<cc@slesvico-holsatia.org>',
    maintainer='Richard Neumann',
    maintainer_email='<mail@richard-neumann.de>',
    packages=[
        'cshsso',
        'cshsso.orm',
        'cshsso.orm.functions',
        'cshsso.wsgi'
    ],
    entry_points={
        'console_scripts': [
            'cshsso-setup-db = cshsso.install:setup_db'
        ],
    },
    description='Corps Slesvico-Holsatia Single-Sign-On Framework.'
)
