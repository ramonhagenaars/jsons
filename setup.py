from setuptools import setup


with open('README.md', 'r') as fh:
    long_description = fh.read()


setup(
    name='jsons',
    version='1.0.0',
    author='Ramon Hagenaars',
    author_email='ramon.hagenaars@gmail.com',
    description='For serializing Python objects to JSON (dicts) and back',
    long_description=long_description,
    long_description_content_type='text/x-rst',
    url='https://github.com/ramonhagenaars/jsons',
    packages=[
        'jsons',
        'jsons.classes',
        'jsons.deserializers',
        'jsons.serializers'
    ],
    install_requires=[
        'typish>=1.2.0'
    ],
    test_suite='tests',
    tests_require=[
        'dataclasses;python_version=="3.6"'
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
        'Programming Language :: Python :: 3.8'
    ]
)
