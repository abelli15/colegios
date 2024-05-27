import re

def find_match(pattern, string):
    match = re.search(pattern, string)
    return match
def find_all_matches(pattern, string):
    matches = re.findall(pattern, string)
    return matches
def replace_text(pattern, replacement, string):
    result = re.sub(pattern, replacement, string)
    return result
def split_text(pattern, string):
    result = re.split(pattern, string)
    return result
def match_pattern(pattern, string):
    match = re.fullmatch(pattern, string)
    return match
