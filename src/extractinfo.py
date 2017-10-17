#!/bin/python3

import re

reference = ['suspect','male']

addr_anchor = ['in','on','around','of']

def matchDate(input):
    pattern = r"\d{1,2}\/\d{1,2}(\/((\d{4})|(\d{2})))?"
    res = re.finditer(pattern,input)
    return res

def matchTime(input):
    pattern = r"(\d{1,2}(:\d{1,2})? ((a\.?m\.?)|(p\.?m\.?)))|noon|midnight"
    res = re.finditer(pattern,input)
    return res

if __name__ == '__main__':
    with open('../mail/crime4.txt', 'r') as content_file:
        content = content_file.read()
    for e in matchDate(content):
        print(e)
    for e in matchTime(content):
        print(e)
