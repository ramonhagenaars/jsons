import attr


@attr.s
class AttrsClass:
    a: str = attr.ib()
    b: int = attr.ib()


@attr.s(auto_attribs=True)
class AttrsClassAutoAttribs:
    a: str
    b: int


@attr.s
class AttrsClassPrivate:
    _a: str = attr.ib()


@attr.s
class AttrsClassPrivateAndDunder:
    _a: str = attr.ib()
    __b__: str = attr.ib()


@attr.s
class AttrsClassDefault:
    a: str = attr.ib(default='standard')


@attr.s
class AttrsClassValidator:
    a: int = attr.ib()

    @a.validator
    def _check(self, attribute, value):
        if value > 10:
            raise ValueError('Cannot be greater than 10')


@attr.s
class AttrsClassConverter:
    a: int = attr.ib(converter=int)
    b: str = attr.ib(converter=int)  # This gets weird.


@attr.s(init=False)
class AttrsClassNoInit:
    a: int = attr.ib()


@attr.s
class AttrsClassNoInitSome:
    a: int = attr.ib()
    b: str = attr.ib(init=False)


@attr.s(frozen=True)
class AttrsClassFrozen:
    a: int = attr.ib()


@attr.s(slots=True)
class AttrsClassSlots:
    a: int = attr.ib()


@attr.s(kw_only=True)
class AttrsClassKwOnly:
    a: int = attr.ib()
