#!/usr/bin/env python
import re
import sys
import json

infile, outfile = "", ""
demo = False
for each in sys.argv:
    if each == "-d":
        demo = True

if len(sys.argv) != 3 and not demo:
    print("Please enter input and output filenames, or -d for demo")
elif not demo:
    infile = sys.argv[1]
    outfile = sys.argv[2]


def from_file(inf):
    with open(inf, 'r') as file:
        for line in file:
            parse_line(line.rstrip('\n').split('\t'))


def parse_line(l):
    currentDict = headDict
    idx = 0
    while idx < len(l):
        if l[idx] != "":
            add_data(currentDict, idx, l)
        else:
            if type(currentDict.get(parentList[idx])) is list:
                currentDict = currentDict.get(parentList[idx][0])[parentList[idx][1]]
            else:
                currentDict = currentDict.get(parentList[idx])
        idx += 1


def add_data(currentDict, idx, l):
    if is_array(l[idx]):
        array_data_piece(currentDict, l[idx], idx)
    else:
        if l[idx].strip() not in currentDict:
            single_data_piece(currentDict, l[idx].strip())
        append_parent_list(idx, l[idx])


def is_array(data):
    return re.match('.*\[\].*', data)


def append_parent_list(idx, keyName):
    if len(parentList) > idx:
        parentList[idx] = keyName
    else:
        parentList.append(keyName)


def single_data_piece(currentDict, data):
    if re.match('.*=.*', data):
        splt = re.match('^([^ ]*) *([^ ]*) *= *(.+)$', data)
        keyName = splt.group(1).strip()
        dataType = splt.group(2).strip()
        value = splt.group(3).strip()
        addKV(currentDict, keyName, dataType, value)
    else:
        currentDict[data] = {}


def array_data_piece(currentDict, data, idx):
    if re.match('.*=.*', data):
        splt = re.match('^([^ \[\]]*) *([\[\]]*) *([^ ]*) *= *(.+)$', data)
        keyName = splt.group(1).strip()
        dataType = splt.group(3).strip()
        value = splt.group(4).strip()
        if keyName not in currentDict:
            currentDict[keyName] = []
        aList = value.split(",")
        for item in aList:
            add_simp_array(currentDict, keyName, dataType, item.strip())
        append_parent_list(idx, keyName)
    else:
        splt = re.match('^([^ \[\]]*) *\[[ ]*[0-9]*[ ]*\]', data)
        keyName = splt.group(1).strip()
        index = splt.group(2).strip()
        if keyName in currentDict:
            while len(currentDict[keyName]) <= index:
                currentDict[keyName].append({})
        else:
            currentDict[keyName] = [0]
            currentDict[keyName][0] = {}
        append_parent_list(idx, [keyName, index])


def addKV(curD, key, dType, val):
    if dType == 'b':
        curD[key] = (val == 'True' or val == 'true')
    elif dType == 'i':
        try:
            curD[key] = int(val)
        except ValueError:
            curD[key] = val
    elif dType == 'f':
        try:
            curD[key] = float(val)
        except ValueError:
            curD[key] = val
    else:
        curD[key] = val


def add_simp_array(curD, key, dType, val):
    if dType == 'b':
        curD[key].append((val == 'True' or val == 'true'))
    elif dType == 'i':
        try:
            curD[key].append(int(val))
        except ValueError:
            curD[key].append(val)
    elif dType == 'f':
        try:
            curD[key].append(float(val))
        except ValueError:
            curD[key].append(val)
    else:
        curD[key].append(val)


def to_file(outf):
    with open(outf, 'w') as file:
        json.dump(headDict, file, indent=5, sort_keys=True)


def main():
    from_file(infile)
    to_file(outfile)


def demo():
    from_file('demo/demo.txt')
    to_file('demo/demo.json')


parentList = []
headDict = {}

if demo:
    demo()
else:
    main()
