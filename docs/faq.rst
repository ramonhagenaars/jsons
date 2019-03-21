
::

       _                     
      (_)                    
       _ ___  ___  _ __  ___ 
      | / __|/ _ \| '_ \/ __|
      | \__ | (_) | | | \__ \
      | |___/\___/|_| |_|___/
     _/ | JSON SERIALIZATION                   
    |__/      MADE EASY!               

      Official Documentation  

##########################
Frequently Asked Questions
##########################

Do I need to use dataclasses?
-----------------------------
No, not necessarily. The following example shows a class that jsons can
serialize and deserialize without a problem:

.. code:: python

    class Person:
        def __init__(self, name: str, car: Car):
            self.name = name
            self.car = car

Do I need to use type hints?
----------------------------
No, not necessarily, (but it is recommended to do so anyway for readability).
Only if your class has an attribute of a custom class type, you need to use a
type hint for proper *deserialization* with jsons. *Serialization* works
always, no matter the presence or absence of type hints.

Here is an example:

.. code:: python

    class Person:
        def __init__(self, name, birthday, car: Car):
            self.name = name
            self.birthday = birthday
            self.car = car

This class does not require type hints for ``name`` and ``birthday`` (assuming
that they are meant to be of type ``str`` and ``datetime`` respectively). The
``Car`` is a custom class though, so that one needs a type hint if you want
deserialization to work.

So in short: only for custom classes and only for deserialization.


Is it possible to discard private attributes?
---------------------------------------------
Yes it is. Use ``strip_privates`` for that.

.. code:: python

    jsons.dump(some_inst, strip_privates=True)

How can I write a custom serializer?
------------------------------------
First create your serializer function. It requires at least the parameters
``obj`` and ``**kwargs``. You may introduce additional parameters to your
liking.

Here is an example:

.. code:: python

    def my_custom_datetime_serializer(obj: datetime,
                                      only_seconds: bool = False,
                                      **kwargs) -> Union[int, float]:
        if only_seconds:
            return int(obj.timestamp())
        return obj.timestamp()

Note: the type hints are *not* required.

Next, you need to register your serializer function with the type you want to
use that serializer function for:

.. code:: python

    jsons.set_serializer(my_custom_datetime_serializer, datetime)

And you're set:

.. code:: python

    >>> my_date = datetime.now(tz=timezone.utc)
    >>> jsons.dump(my_date, only_seconds=True)
    1552819054

How can I write a custom deserializer?
--------------------------------------
First create your deserializer function. It requires at least the parameters
``obj``, ``cls`` and ``**kwargs``. You may introduce additional parameters to
your liking.

Here is an example:

.. code:: python

    def my_custom_datetime_deserializer(obj: Union[int, float],
                                        cls: type = datetime,
                                        **kwargs) -> datetime:
        return datetime.fromtimestamp(ts)

Note: the type hints are *not* required.

Next, you need to register your deserializer function with the type you want to
use that deserializer function for:

.. code:: python

    jsons.set_deserializer(my_custom_datetime_deserializer, datetime)

And you're set:

.. code:: python

    >>> jsons.load(1552819054, datetime)
    datetime.datetime(2019, 3, 17, 11, 37, 34)

Why does jsons tolerate additional attributes in my json object compared to the class?
--------------------------------------------------------------------------------------
The thoughts on this are as follows:

- jsons was designed to be very tolerant by default.
- jsons is in fact capable of deserializing json data into a class with fewer attributes; all required fields were provided. So it is reasonable that no error should occur.
- jsons should be compatible with json schemas and they allow extra attributes by default as well.

You can however turn 'strict-mode' on:

.. code:: python

    jsons.load(some_json, cls=SomeClass, strict=True)

By doing so, any mismatch between the json object and the class results in a ``DeserializationError``.


How can I deserialize without exactly knowing the target class?
---------------------------------------------------------------
Sometimes you do not know beforehand of which exact class you have a json
instance.

There are two ways to deal with this. The first is to use a ``Union`` and
define all possible types that you want to deserialize to:

.. code:: python

    jsons.load(car_json, Union[Audi, Porche, Tesla], strict=True)

The possible classes are examined from left to right and the first successful
deserialization is returned.

The second option is to serialize verbose objects:

.. code:: python

    car_json = jsons.dump(car_inst, verbose=True)

When loading a verbose object, you may omit the expected class:

.. code:: python

    car_inst = jsons.load(car_json)

Why not just use ``__dict__``?
------------------------------
For the following reasons:

* The __dict__ attribute only creates a shallow dict of an instance. Any contained object is not serialized to a dict.
* The __dict__ does not take @property methods in account.
* Not all objects have a __dict__ attribute (e.g. datetime does not).
* The serialization process of __dict__ cannot easily be tuned.
* There is no means to deserialize with __dict__.

Why not use the standard ``json`` library?
------------------------------------------
For the following reasons:

* It's quite a hassle to (de)serialize custom types: you need to write a subclass of json.JSONEncoder with specific serialization/deserialization code per custom class.
* You will need to provide that subclass of json.JSONEncoder to json.dumps/json.loads every single time.

Aren't there already libraries for serialization to json?
---------------------------------------------------------
There are.

Here is how ``jsonpickle`` serializes a ``datetime``:


.. code:: python

   >>> jsonpickle.encode(my_date)
   '{"py/object": "datetime.datetime", "__reduce__": [{"py/type": "datetime.datetime"}, ["B+MDEBUYLgVu1w=="]]}'

And this is how ``jsons`` does it:

.. code:: python

   >>> jsons.dumps(my_date)
   '"2019-03-16T21:24:46.356055+01:00"'

And this is what ``marshmallow`` requires your classes to look like:

.. code:: python

    class AlbumSchema(Schema):
        title = fields.Str()
        release_date = fields.Date()
        artist = fields.Nested(ArtistSchema())

Compare that to ``jsons``:

.. code:: python

    class AlbumSchema:
        def __init__(self, title: str, release_date: datetime, artist: Artist)
            self.title = title
            self.release_date = release_date
            self.artist = artist

    # Or even better, using a dataclass:

    @dataclass
    class AlbumSchema:
            title: str
            release_date: datetime
            artist: Artist

And this is what a ``serpy`` serializer for your custom class looks like:

.. code:: python

    class FooSerializer(serpy.Serializer):
        """The serializer schema definition."""
        # Use a Field subclass like IntField if you need more validation.
        x = serpy.IntField()
        y = serpy.Field()
        z = serpy.Field()

Compared to that of ``jsons``:

.. code:: python

    # Not Necessary at all.

So yes. There are already libraries for serializing Python to json. There may
be some advantages for each library, so you should do your homework.

My json contains camelcase, how can I transform to the right case?
------------------------------------------------------------------
You can have the keys transformed by the serialization or deserialization
process by providing a transformer function that takes a string and returns a
string.

.. code:: python

    result = jsons.dump(some_obj, key_transformer=jsons.KEY_TRANSFORMER_CAMELCASE)
    # result could be something like: {'thisIsTransformed': 123}

    result = jsons.load(some_dict, SomeClass,
                        key_transformer=jsons.KEY_TRANSFORMER_SNAKECASE)
    # result could be something like: {'this_is_transformed': 123}

The following casing styles are supported:

.. code:: python

    KEY_TRANSFORMER_SNAKECASE   # snake_case
    KEY_TRANSFORMER_CAMELCASE   # camelCase
    KEY_TRANSFORMER_PASCALCASE  # PascalCase
    KEY_TRANSFORMER_LISPCASE    # lisp-case


How do the jsons decorators work?
---------------------------------
Use ``loaded`` to automatically apply ``jsons.load`` to the parameters and/or
the return value.

Here is an example:

.. code:: python

    from datetime import datetime
    from jsons.decorators import loaded


    @loaded()
    def some_func(x: datetime) -> datetime:
        # x is now of type datetime.
        return '2018-10-07T19:05:00+02:00'

    result = some_func('2018-10-07T19:05:00+02:00')
    # result is now of type datetime.

In the above case, the type hint could be omitted for the same result: jsons
will recognize the timestamp from the string automatically. In case of a custom
type, you do need a type hint. The same goes for the return type; it could be
omitted in this case as well.

Similarly, you can decorate a function or method with ``@dumped`` as is done
below:

.. code:: python

    from datetime import datetime
    from jsons.decorators import dumped


    class SomeClass:
        @classmethod
        @dumped()
        def some_meth(cls, x):
            # x is now of type str, cls remains untouched.
            return datetime.now()

    result = SomeClass.some_meth(datetime.now())
    # result is now of type str.

In case of methods, like in the example above, the special self or cls
parameters are not touched by the decorators ``@loaded()`` or ``@dumped()``.
Additionally, you can provide a type hint for any parameter (except self or
cls) or the return value. Doing so will make jsons attempt to dump into that
particular type, just like with ``jsons.dump(some_obj, cls=ParticularType)``.

For more info, see the
`api doc <https://jsons.readthedocs.io/en/latest/api.html#decorators>`_.

Can I just participate in discussions on the issues?
----------------------------------------------------
Yes, please do. Your opinion is highly valuated and appreciated.

I have an idea for a new feature, what should I do?
---------------------------------------------------
Please always check the API first, maybe your feature was already there. :-)
Otherwise, open up an `issue <https://github.com/ramonhagenaars/jsons/issues>`_
and describe your desired feature and why one would want this.

You can also open a
`pull request <https://github.com/ramonhagenaars/jsons/pulls>`_. It is
advised to first open a discussion in an issue though.

I found a bug, what should I do?
--------------------------------
Please report bugs by opening an
`issue <https://github.com/ramonhagenaars/jsons/issues>`_ on the Github page.

My question is not listed here!
-------------------------------
I'm sorry for that. Please open up an
`issue <https://github.com/ramonhagenaars/jsons/issues>`_ on the Github page.
