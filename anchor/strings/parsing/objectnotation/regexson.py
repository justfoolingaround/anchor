"""
quickson but for the masterclass users; using regex.

This **can** get out of hand.
"""

import re

SYNTAX_SEPARATOR_REGEX = re.compile(r"(?:[^/]|\\/)+")


def iter_regexson_matches(data, *regexsons):

    if not regexsons:
        yield data
        return

    if not isinstance(data, (list, dict)):
        raise TypeError("Data must be a dict or list")

    worker, *rest = regexsons

    if isinstance(data, list):

        if not worker.isdigit():
            raise ValueError("List index must be an integer")

        yield from iter_regexson_matches(data[int(worker)], *rest)
    else:
        for (key, value) in data.items():
            regexp = re.compile(worker)

            if regexp.match(key):
                yield from iter_regexson_matches(value, *rest)


def iter_regexson_matches_from_string(regexson_string, data):
    """
    Iterate over the matches of a regexson string.
    """
    yield from iter_regexson_matches(
        data, *SYNTAX_SEPARATOR_REGEX.findall(regexson_string)
    )
