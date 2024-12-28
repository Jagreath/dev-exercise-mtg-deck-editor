from re import compile as re_compile

_moxfield_decklist_pattern = re_compile(r"\s*(?P<quant>\d+)\s+(?P<name>[\d\w\s\-\,\'\/]+)\s+\((?P<set>[\d\w]{3,4})\)\s+(?P<num>[\d\w\-★]{1,7})\s*")

def parse_moxfield_string(string: str) -> tuple[str, str, str, int]:
    """
    Parse a string representing card records in a format used by Moxfield.
    
    ex. 1 Card Name (SET) NUMBER

    arguments:
    string -- a card entry

    returns:
    tuple -- name, set code, collector number, quantity
    """
    if string is not None:
        match = _moxfield_decklist_pattern.match(string)
        if match:
            return (match.group("name").strip(),
                    match.group("set").strip(),
                    match.group("num").strip(),
                    int(match.group("quant").strip()))
    return None