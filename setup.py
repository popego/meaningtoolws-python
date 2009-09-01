#!/usr/bin/env python
# -*- coding: utf8 -*-

#try:
#    from setuptools import setup, find_packages
#except ImportError:
#    from ez_setup import use_setuptools
#    use_setuptools()
#    from setuptools import setup, find_packages



#setup(name='meaningtoolws',
#      version='0.1',
#      author='Popego Corporation',
#      url='http://github.com/k0001/meaningtoolws',
#      packages=['src/meaningtoolws'],
#     )

import os
try:
    from setuptools import setup, find_packages, Extension
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages, Extension

import os.path
src_folder= os.path.join(
    os.path.split(os.path.abspath(__file__))[0], 'src')
setup(
    name='meaningtoolws',
    version="0.3",
    description='Meaningtool Web Services Python Client',
    author='Popego Team',
    author_email='contact@popego.com',
    url='',
    install_requires=[ ],
    tests_require=[
            'nose'
            ],
    package_dir= {'' : 'src' },
    packages=find_packages(where=src_folder, exclude=['test', 'test.*']),
#    ext_package='utils',
    include_package_data=True,
    test_suite='nose.collector',
    entry_points="""""",
    zip_safe=False
)


