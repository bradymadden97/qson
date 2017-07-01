#!/usr/bin/env python
# __author__bradymadden97__

import re
import sys
import json
import warnings

infile, outfile = "", ""
demo_flag = False
for each in sys.argv:
    if each == "-d":
        demo_flag = True

if len(sys.argv) != 3 and not demo_flag:
    raise RuntimeError("Please enter input and output filenames, or -d for demo")
elif not demo_flag:
    infile = sys.argv[1]
    outfile = sys.argv[2]


def from_file(inf):
    with open(inf, 'r') as file:
        for line in file:
            parse_line(line.rstrip('\n').rstrip().replace("    ", "\t").split("\t"))


def parse_line(l):
    if handle_empty(l):
        return
    current_dict = headDict
    idx = 0
    while idx < len(l):
        if l[idx] != "":
            add_data(current_dict, idx, l)
        else:
            if type(current_dict.get(parentList[idx].name)) is list:
                current_dict = current_dict.get(parentList[idx].name)[parentList[idx].index]
            else:
                current_dict = current_dict.get(parentList[idx].name)
                handle_invalid(current_dict, parentList[idx].name)
        idx += 1


def handle_empty(entry):
    return len(entry) == 1 and entry[0] == ""


def handle_invalid(current_dict, last):
    if current_dict is None:
        errstr = str("Syntax error. '" + last + "' cannot have both a value and children nodes.")
        raise SyntaxError(errstr)


def add_data(current_dict, idx, l):
    current_key = l[idx]
    if is_simple_array(current_key):
        array_data_piece(current_dict, current_key, idx)
    elif is_object_array(current_key):
        current_key, index = object_array_data_piece(current_dict, current_key, idx)
        append_parent_list(idx, current_key, index)
    else:
        if current_key.strip() not in current_dict:
            current_key = single_data_piece(current_dict, current_key.strip())
        append_parent_list(idx, current_key, None)


def is_simple_array(data):
    return re.match('.*\[\].*', data)


def is_object_array(data):
    return re.match('.*\[[0-9]+\].*', data)


def append_parent_list(idx, key_name, index):
    pln = create_parent_list_node(key_name, index)
    if len(parentList) > idx:
        parentList[idx] = pln
    else:
        parentList.append(pln)


def single_data_piece(current_dict, data):
    if re.match('.*=.*', data):
        splt = re.match('^([^ ]*) *([^ ]*) *= *(.+)$', data)
        key = splt.group(1).strip()
        data_type = splt.group(2).strip()
        value = splt.group(3).strip()
        return add_key_val(current_dict, key, data_type, value)
    else:
        new_key = validate_key(data)
        current_dict[new_key] = {}
        return new_key


def array_data_piece(current_dict, data, idx):
    if re.match('.*=.*', data):
        splt = re.match('^([^ \[\]]*) *([\[\]]*) *([^ ]*) *= *(.+)$', data)
        key = splt.group(1).strip()
        data_type = splt.group(3).strip()
        value = splt.group(4).strip()
        new_key = validate_key(key)
        if new_key not in current_dict:
            current_dict[new_key] = []
        a_list = value.split(",")
        for item in a_list:
            add_simp_array(current_dict, new_key, data_type, item.strip())
        append_parent_list(idx, new_key, None)
    else:
        splt = re.match('^([^ \[\]]*)', data)
        key = validate_key(splt.group(1).strip())
        if key not in current_dict:
            current_dict[key] = []
        append_parent_list(idx, key, None)


def object_array_data_piece(current_dict, data, idx):
    splt = re.match('^([^ \[\]]*) *\[[ ]*([0-9]+)[ ]*\]', data)
    key = splt.group(1).strip()
    index = int(splt.group(2).strip())
    new_key = validate_key(key)
    if new_key in current_dict:
        if len(current_dict[new_key]) <= index:
            add_object_array_index(current_dict[new_key], len(current_dict[new_key]), index)
    else:
        current_dict[new_key] = []
        add_object_array_index(current_dict[new_key], 0, index)
    return new_key, index


def add_object_array_index(current_array, start, idx):
    while start <= idx:
        current_array.append({})
        start += 1


def add_key_val(cur_dict, k, data_type, val):
    key = validate_key(k)
    if data_type == 'b':
        cur_dict[key] = (val == 'True' or val == 'true')
    elif data_type == 'i':
        try:
            cur_dict[key] = int(val)
        except ValueError:
            cur_dict[key] = val
    elif data_type == 'f':
        try:
            cur_dict[key] = float(val)
        except ValueError:
            cur_dict[key] = val
    elif data_type == 's':
        cur_dict[key] = val
    else:
        invalid_data_type(key, data_type)
        cur_dict[key] = val
    return key


def validate_key(key):
    new_key = re.match('^[^ \t\n]*', key).group(0)
    if new_key != key:
        errmsg = str("Key '" + key + "' cannot have spaces. Adjusted to '" + new_key + "'")
        warnings.warn(errmsg, SyntaxWarning)
    if new_key[0].isupper():
        newer_key = str(new_key[0].lower() + new_key[1:])
        errmsg = str("Key '" + new_key + "' cannot begin with uppercase. Adjusted to '" + newer_key + "'")
        warnings.warn(errmsg, SyntaxWarning)
        return newer_key
    return new_key


def add_simp_array(cur_dict, key, data_type, val):
    if data_type == 'b':
        cur_dict[key].append((val == 'True' or val == 'true'))
    elif data_type == 'i':
        try:
            cur_dict[key].append(int(val))
        except ValueError:
            cur_dict[key].append(val)
    elif data_type == 'f':
        try:
            cur_dict[key].append(float(val))
        except ValueError:
            cur_dict[key].append(val)
    elif data_type == 's':
        cur_dict[key].append(val)
    else:
        invalid_data_type(key, data_type)
        cur_dict[key].append(val)


def invalid_data_type(key, dt):
    if dt != "":
        errmsg = ""
        if len(dt) > 1:
            errmsg = str("Key '" + key + "' cannot have spaces. '" + dt + "' is also not a valid data type.")
        else:
            errmsg = str("Data type '" + dt + "' is not a valid data type for key '" + key + "'")
        warnings.warn(errmsg, SyntaxWarning)


def to_file(outf):
    with open(outf, 'w') as file:
        json.dump(headDict, file, indent=5, sort_keys=True)


def main():
    from_file(infile)
    to_file(outfile)


def demo():
    from_file('demo/demo.txt')
    to_file('demo/demo.json')


class ParentListNode(object):
    name = ""
    index = None

    def __init__(self, name, index):
        self.name = name
        self.index = index


def create_parent_list_node(name, index):
    pln = ParentListNode(name, index)
    return pln



parentList = []
object_list_index = 0
headDict = {}


if demo_flag:
    demo()
else:
    main()
