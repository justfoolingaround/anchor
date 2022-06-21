from typing import Callable, Iterable, TypeVar

import re

search_type = TypeVar("search_type")


def iter_regex_results(
    query: "str",
    possibilities: "Iterable[search_type]",
    *,
    processor: "Callable[[search_type], str] | None" = None
):
    """
    Use regex to search for a string in a list of possibilities.

    :param query: The query to search for.
    :param possibilities: The list of possibilities to search in.
    :param processor: A function to process each possibility.

    :yield: The matching possibilities, level of match.
    """
    pattern = re.compile(
        r"(.*?)".join(map(re.escape, query.strip())) + r"(.*)", flags=re.IGNORECASE
    )

    for raw_search_value in possibilities:

        if processor is not None:
            search_value = processor(raw_search_value)
        else:
            search_value = raw_search_value

        match = pattern.match(search_value)

        if match:
            yield search_value, (1 - sum(map(len, match.groups())) / len(search_value))
