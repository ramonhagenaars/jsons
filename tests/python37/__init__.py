try:
    from dataclasses import dataclass


    @dataclass
    class Person:
        name: str
except:
    pass
