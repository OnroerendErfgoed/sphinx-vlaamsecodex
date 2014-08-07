# -*- coding: utf-8 -*-
#!/usr/bin/env python

from setuptools import setup
requires = ['requests']

setup(
    name='sphinx-vlaamsecodex',
    version='0.0',
    url='https://github.com/OnroerendErfgoed/sphinx-vlaamsecodex',
    license='MIT',
    author='Flanders Heritage Agency',
    author_email='ict@onroerenderfgoed.be',
    description='Sphinx extension to integrate http://codex.vlaanderen.be in a document.',
    long_description=open('README.md').read(),
    include_package_data=True,
    zip_safe=False,
    packages=['sphinx-oe'],
    install_requires=requires,
    classifiers=[
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Topic :: Documentation',
        'Topic :: Software Development :: Documentation',
      ]
)
