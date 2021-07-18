import os
from setuptools import setup


here = os.path.abspath(os.path.dirname(__file__))
meta_info = {}
with open(os.path.join(here, 'jsons', '_meta.py'), 'r') as f:
    exec(f.read(), meta_info)

with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name=meta_info['__title__'],
    version=meta_info['__version__'],
    author=meta_info['__author__'],
    author_email=meta_info['__author_email__'],
    description=meta_info['__description__'],
    url=meta_info['__url__'],
    long_description=long_description,
    long_description_content_type='text/markdown',
    license=meta_info['__license__'],
    packages=[
        'jsons',
        'jsons.classes',
        'jsons.deserializers',
        'jsons.serializers'
    ],
    install_requires=[
        'typish>=1.9.2'
    ],
    python_requires='>=3.5',
    test_suite='tests',
    tests_require=[
        'dataclasses;python_version=="3.6"',
        'tzdata;python_version>="3.9"'
    ],
    zip_safe=False,
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9'
    ]
)
