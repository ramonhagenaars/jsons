from setuptools import setup

with open('README.rst', 'r') as fh:
    long_description = fh.read()

setup(name='jsons',
      version='0.5.5',
      author='Ramon Hagenaars',
      author_email='ramon.hagenaars@gmail.com',
      description='For serializing Python objects to JSON (dicts) and back',
      long_description=long_description,
      long_description_content_type='text/x-rst',
      url='https://github.com/ramonhagenaars/jsons',
      packages=['jsons'],
      zip_safe=False,
      classifiers=(
          'Programming Language :: Python :: 3',
          'Operating System :: OS Independent'
      )
)
