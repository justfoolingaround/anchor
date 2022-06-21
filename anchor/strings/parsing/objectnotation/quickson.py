import re

SYNTAX_SEPARATOR_REGEX = re.compile(r"(?:[^/]|\\/)+")

exceptions = (
    IndexError,
    KeyError,
    TypeError,
    ValueError,
)


def quickson_navigator(data, *quicksons):

    while quicksons:

        if not isinstance(data, (list, dict)):
            raise TypeError("Data must be a dict or list")

        worker, *rest = quicksons

        if isinstance(data, list):
            if not worker.isdigit():
                raise ValueError("List index must be an integer")

            data = data[int(worker)]
        else:
            data = data[worker]

        quicksons = rest

    return data


def navigate_quickson(quickson_string, data, default=None):
    """
    A function that navigates through a quickson string and returns the data from
    the data dictionary.
    """

    try:
        return quickson_navigator(
            data, *SYNTAX_SEPARATOR_REGEX.findall(quickson_string)
        )
    except exceptions as _:
        if default is None:
            raise _

    return default


if __name__ == "__main__":
    # fmt: off
    assert navigate_quickson("a/b/c", {"a": {"b": {"c": "d"}}}) == "d"
    assert navigate_quickson("a/b/c/0", {"a": {"b": {"c": ["d"]}}}) == "d"
    assert navigate_quickson("a/b/c/0/1", {"a": {"b": {"c": [{"d": []}]}}}, "test") == "test"
    # fmt: on
