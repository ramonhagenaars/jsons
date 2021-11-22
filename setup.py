import os
from setuptools import setup


here = os.path.abspath(os.path.dirname(__file__))
meta_info = {}
with open(os.path.join(here, 'jsons', '_package_info.py'), 'r') as f:
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
        'jsons.serializers',
    ],
    python_requires='>=3.5',
    install_requires=[
        'typish>=1.9.2',
    ],
    extras_require={
        'test': [
            'dataclasses;python_version=="3.6"',
            'tzdata;python_version>="3.9"',
            'attrs',
            'coverage',
            'codecov',
            'pytest',
            'scons',
        ]
    },
    test_suite='tests',
    zip_safe=False,
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        *['Programming Language :: Python :: {}'.format(version)
          for version in meta_info['__python_versions__']],
    ]
)
