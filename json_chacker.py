# ! /usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function
import json

from lib.my_convertor import dfs_dict
from lib.my_marshal import marshal

type_convert_config = 'data/swagger_test.json'
# api_mapping = {"device_info": "Device", "event_info": "Event", "ip_info": "IpInfo"}
api_mapping = {}


def gen_format_converter(api_mapping=None):
    with open(type_convert_config, 'r') as fr:
        api_def_json = json.load(fr)
    api_definitions = api_def_json.get("definitions", {})
    ret_dict = {}
    if api_mapping:
        for api_node, config_node in api_mapping.items():
            ret_dict[api_node] = dfs_dict(api_definitions[config_node], api_definitions)
    else:
        for api_node, config_node in api_definitions.items():
            ret_dict[api_node] = dfs_dict(config_node,api_definitions)
    return ret_dict


api_field_dict = gen_format_converter(api_mapping)


def convert(post_body, format_type, api_mapping=api_mapping, api_field_dict=api_field_dict):
    return json.loads(json.dumps((marshal(post_body, {api_mapping.get(format_type): api_field_dict.get(format_type)}))))


if __name__ == '__main__':
    print(json.dumps(dict(marshal({'Order': {"id": '123'}}, {'Order': api_field_dict.get('Order')}))))
