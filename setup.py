#! /usr/bin/env python3
"""Install scipt."""

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
    author_email='<cc@slesvico-holsatia.orf>',
    maintainer='Richard Neumann',
    maintainer_email='<mail@richard-neumann.de>',
    packages=[
        'cshsso',
        'cshsso.wsgi'
    ],
    description='Corps Slesvico-Holsatia Single-Sign-On Framework.'
)
