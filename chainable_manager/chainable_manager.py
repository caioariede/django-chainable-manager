from django.db.models.query import QuerySet
from django.db.models import Manager

import types


def chainable_manager(cls):
    class ChainableQuerySet(QuerySet):
        pass

    def chainable_queryset(self):
        return ChainableQuerySet(self.model, using=self._db)

    # List methods defined in `cls`
    methods = set(dir(cls)) - (set(dir(cls.__mro__[1])) & set(dir(cls)))

    # In the case you have override the `get_query_set` method
    # you must call: `self.get_chainable_query_set()`,
    # instead of: `super(YourManager, self).get_query_set()`
    cls.get_chainable_query_set = chainable_queryset

    # Some validation to prevent mistakes
    assert len(cls.__mro__) > 1 and issubclass(cls, Manager), \
        "The @chainable_manager must wrap a subclass of %s, not %s" % (
            Manager, cls.__mro__[1])

    if cls.__mro__[1].get_query_set == cls.get_query_set:
        # Only replaces `get_query_set` if it was not inherited
        cls.get_query_set = cls.get_chainable_query_set

    # Remove methods on Manager and install on ChainableQuerySet
    for method in methods:
        setattr(ChainableQuerySet, method, types.MethodType(
            getattr(cls, method).__func__, None, ChainableQuerySet))

        delattr(cls, method)

    # Install __getattr__
    def __getattr(self, name):
        return getattr(self.get_query_set(), name, None) \
            or getattr(cls, name)

    setattr(cls, '__getattr__', types.MethodType(__getattr, None, cls))

    return cls
