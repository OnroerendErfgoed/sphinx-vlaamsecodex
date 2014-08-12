# -*- coding: utf-8 -*-
#!/usr/bin/env python

from setuptools import setup, find_packages
requires = ['requests']

setup(
    name='sphinx-vlaamsecodex',
    version='0.1',
    url='https://github.com/OnroerendErfgoed/sphinx-vlaamsecodex',
    license='MIT',
    author='Flanders Heritage Agency',
    author_email='ict@onroerenderfgoed.be',
    description='Sphinx extension to integrate http://codex.vlaanderen.be in a document.',
    long_description=open('README.md').read(),
    zip_safe=False,
    classifiers=[
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Topic :: Documentation',
        'Topic :: Software Development :: Documentation',
      ],
    platforms='any',
    packages=find_packages(),
    package_data={'': ['README.md']},
    include_package_data=True,
    install_requires=requires,
)
