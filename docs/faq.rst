
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

Is it possible to discard private attributes?
---------------------------------------------
Yes it is. Use ``strip_privates`` for that.

.. code:: python

    jsons.dump(some_inst, strip_privates=True)

How can I enforce jsons to raise an error when deserializing fails?
-------------------------------------------------------------------
By turning on 'strict-mode':

.. code:: python

    jsons.load(some_json, cls=SomeClass, strict=True)


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

My question is not listed here!
-------------------------------
I'm sorry for that. Please open up an issue on the Github page.
