.. jsons documentation master file, created by
   sphinx-quickstart on Sat Mar 16 19:55:07 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.


|PyPI version| |Code Coverage| |Scrutinizer Code Quality|

*~ Any Python objects to/from JSON, easily! ~*

Jsons is a library that allows you to serialize your plain old Python objects
to readable json (dicts or strings) and deserialize them back. No magic, no
special types, no polluting your objects. Just you, Python and clean json.

:ref:`search`

********
Features
********
- Python 3.5+
- Minimal effort to use!
- No magic, just you, Python and jsons!
- Human readible JSON without pollution!
- Easily customizable and extendable!
- Type hints for the win!

********************
Installing and using
********************

Install with pip:

::

   pip install jsons

And then you're ready to go:

.. code:: python

   import jsons

   @dataclass
   class Car:
       color: str
       owner: str

   dumped = jsons.dump(Car('red', 'Guido'))

The value of ``dumped``:

.. code:: python

   {'color': 'red', 'owner': 'Guido'}

And to deserialize, just do:

.. code:: python

   instance = jsons.load(loaded, Car)

Type hints for the win!

***
FAQ
***

.. toctree::
   :maxdepth: 5

   faq

***
API
***

.. toctree::
   :maxdepth: 5

   api


.. |PyPI version| image:: https://badge.fury.io/py/jsons.svg
   :target: https://badge.fury.io/py/jsons

.. |Docs| image:: https://readthedocs.org/projects/jsons/badge/?version=latest
   :target: https://jsons.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status

.. |Build Status| image:: https://api.travis-ci.org/ramonhagenaars/jsons.svg?branch=master
   :target: https://travis-ci.org/ramonhagenaars/jsons

.. |Code Coverage| image:: https://codecov.io/gh/ramonhagenaars/jsons/branch/master/graph/badge.svg
  :target: https://codecov.io/gh/ramonhagenaars/jsons

.. |Scrutinizer Code Quality| image:: https://scrutinizer-ci.com/g/ramonhagenaars/jsons/badges/quality-score.png?b=master
   :target: https://scrutinizer-ci.com/g/ramonhagenaars/jsons/?branch=master

.. |Maintainability| image:: https://api.codeclimate.com/v1/badges/17d997068b3387c2f2c3/maintainability
   :target: https://codeclimate.com/github/ramonhagenaars/jsons/maintainability
