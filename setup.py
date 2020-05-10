# -*- coding: utf-8 -*-

# Learn more: https://github.com/kennethreitz/setup.py

from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='pyvideoquality',
    version='0.1.0',
    description='Simple video/image quality metrics as a package',
    long_description=readme,
    author='Ryan Collins',
    author_email='ryan@ohmgeek.co.uk',
    url='https://github.com/OhmGeek/video-quality',
    license=license,
    packages=find_packages(exclude=('tests', 'docs', 'demo'))
)