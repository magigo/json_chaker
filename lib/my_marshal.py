# ! /usr/bin/python
# -*- coding: utf-8 -*-
try:
    from collections import OrderedDict
except ImportError:
    from ordereddict import OrderedDict


def marshal(data, fields, envelope=None):
    """Takes raw data (in the form of a dict, list, object) and a dict of
    fields to output and filters the data based on those fields.
    :param data: the actual object(s) from which the fields are taken from
    :param fields: a dict of whose keys will make up the final serialized
                   response output
    :param envelope: optional key that will be used to envelop the serialized
                     response
    >>> from lib.my_marshal import marshal
    >>> from lib import fields
    >>> data = { 'a': 100, 'b': 'foo' }
    >>> mfields = { 'a': fields.Raw }
    >>> marshal(data, mfields)
    OrderedDict([('a', 100)])
    >>> marshal(data, mfields, envelope='data')
    OrderedDict([('data', OrderedDict([('a', 100)]))])
    """

    def make(cls):
        if isinstance(cls, type):
            return cls()
        return cls
    if isinstance(data, (list, tuple)):
        return (OrderedDict([(envelope, [marshal(d, fields) for d in data])])
                if envelope else [marshal(d, fields) for d in data])
    items = ((k, marshal(data, v) if isinstance(v, dict) else make(v).output(k, data)) for k, v in fields.items())
    return OrderedDict([(envelope, OrderedDict(items))]) if envelope else OrderedDict(items)


if __name__ == '__main__':
    pass
