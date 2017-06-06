# ! /usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function

import arrow
import arrow.parser

from lib import fields


class DateToInteger(fields.Integer):
    def __init__(self, default=0, **kwargs):
        super(DateToInteger, self).__init__(default=default, **kwargs)

    def format(self, value):
        try:
            if value is None:
                return self.default
            if type(value).__name__ == 'int':
                return value
            else:
                if not value.strip():
                    return self.default
                return arrow.get(value).timestamp
        except (ValueError, arrow.parser.ParserError) as ve:
            raise fields.MarshallingException(ve)


def dfs_dict(node, api_definitions=None):
    type_format = node.get("format")
    attribute = node.get('attribute')
    node_type = type_format if type_format == 'timestamp' else node.get("type")
    if not node_type:
        ref = node.get('$ref')
        _prefix, ref_node = ref.rsplit('/', 1)
        assert _prefix == '#/definitions' and api_definitions
        return dfs_dict(api_definitions[ref_node])
    if node_type == "object":
        nest_dict = {}
        sub_properties = node.get("properties")
        if not sub_properties:
            return fields.Raw(attribute=attribute)
        for subnode in sub_properties.items():
            nest_dict[subnode[0]] = dfs_dict(subnode[1], api_definitions)
        return fields.Nested(nest_dict, attribute=attribute)
    elif node_type == "array":
        return fields.List(dfs_dict(node.get("items"), api_definitions), attribute=attribute, default=[])
    elif node_type == 'string':
        return fields.String(default='', attribute=attribute)
    elif node_type == 'integer':
        return fields.Integer(default=-1, attribute=attribute)
    elif node_type == 'timestamp':
        return DateToInteger(default=0, attribute=attribute)
    elif node_type == 'boolean':
        return fields.Boolean(attribute=attribute)
    else:
        raise TypeError(str(node_type) + 'not definition')


if __name__ == '__main__':
    pass
