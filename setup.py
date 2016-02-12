#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

PACKAGES_DATA = {}


INSTALL_REQUIRES = ['psycopg2', 'lxml']

setup(name='notes2pg',
      description='Import OpenStreetMap notes to Postgers',
      author='Xavier Barnada Rius',
      author_email='xbarnada@gmail.com',
      version='0.1.0',
      license='General Public Licence 2',
      long_description='''Import OpenStreetMap notes to Postgers''',
      provides=['notes2pg'],
      install_requires=INSTALL_REQUIRES,
      packages=find_packages(),
      package_data=PACKAGES_DATA,
      entry_points={
          'console_scripts': [
              'notest2pg = cli.notes2pg:main'
          ]
      })
