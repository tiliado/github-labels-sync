# Copyright 2018 Jiří Janoušek <janousek.jiri@gmail.com>
# Licensed under BSD-2-Clause license - see file LICENSE for details.

from typing import Union, Dict


def get_str_dict(data: dict, key: str) -> Union[Dict[str, str], None]:
    item = data.get(key)
    if item is None:
        return None
    if not isinstance(item, dict):
        raise TypeError(f'{key}: A dict expected, not {type(item)!s} {item!r}.')
    for key2, value2 in item.items():
        if not isinstance(key2, str):
            raise TypeError(f'{key}: Key must be str, not {type(key2)!s} {key2!r}.')
        if not isinstance(value2, str):
            raise TypeError(f'{key}.{key2}: Value must be str, not {type(value2)!s} {value2!r}.')
    return item


def get_str_dict_of_str_dicts(data: dict, key: str) -> Union[Dict[str, Dict[str, str]], None]:
    item = data.get(key)
    if item is None:
        return None
    if not isinstance(item, dict):
        raise TypeError(f'{key}: A dict expected, not {type(item)!s} {item!r}.')
    for key2, value2 in item.items():
        if not isinstance(key2, str):
            raise TypeError(f'{key}: Key must be str, not {type(key2)!s} {key2!r}.')
        if not isinstance(value2, dict):
            raise TypeError(f'{key}.{key2}: Value must be a dict, not {type(value2)!s} {value2!r}.')
        for key3, value3 in value2.items():
            if not isinstance(key3, str):
                raise TypeError(f'{key}.{key2}: Key must be str, not {type(key3)!s} {key3!r}.')
            if not isinstance(value3, str):
                raise TypeError(f'{key}.{key2}.{key3}: Value must be str, not {type(value3)!s} {value3!r}.')
    return item
