import re


def iter_conditions(string, media_matchers=r"[0-9.]", media_separators=r"[:=-]"):
    """
    Iterate over the range conditions in a string.
    """
    if not string:
        yield lambda _: True

    regexp = re.compile(
        rf"(?:(?P<start>{media_matchers}*)(?P<separator>{media_separators}))?(?P<end>{media_matchers}+)"
    )

    for match in regexp.finditer(string):

        start, end = (float(_) if _ else None for _ in match.group("start", "end"))

        contains_separator = match.group("separator") is not None

        if not start:
            if contains_separator:
                yield lambda value, end=end: value <= end
            else:
                yield lambda value, end=end: value == end

        else:
            if start > end:
                start, end = end, start

            yield lambda value, start=start, end=end: start <= value <= end


def match_conditions(
    value,
    condition_string,
    selection_func=any,
    *,
    media_matchers=r"[0-9.]",
    media_separators=r"[:=-]",
):
    """
    Match a value against a list of conditions.
    """
    return selection_func(
        condition(value)
        for condition in iter_conditions(
            condition_string, media_matchers, media_separators
        )
    )
