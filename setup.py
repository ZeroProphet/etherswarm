#!/usr/bin/env python
import os
from setuptools import setup, find_packages, Extension


here = os.path.abspath(os.path.dirname(__file__))

install_requires = [
    line
    for line in open(
        os.path.join(here, "requirements.txt"),
        "r"
    )
]

setup(name='EtherSwarm',
      version='0.1',
      description='Manage your ether addresses',
      author='Elder Ryan',
      license='GPL',
      author_email='ryankung@ieee.org',
      packages=['etherswarm'],
      url='https://github.com/ZeroProphet/etherswarm',
      install_requires=install_requires,
      entry_points={
          "console_scripts": [
              "etherswarm=etherswarm:main"
          ]
      }
     )
