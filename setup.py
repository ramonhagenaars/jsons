from setuptools import setup

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(name='jsons',
      version='0.2.0',
      author='Ramon Hagenaars',
      description='For serializing Python objects to JSON and back',
      long_description=long_description,
      long_description_content_type='text/markdown',
      url='https://github.com/ramonhagenaars/jsons',
      py_modules=['jsons'],
      zip_safe=False,
      classifiers=(
          'Programming Language :: Python :: 3',
          'Operating System :: OS Independent'
      )
)
