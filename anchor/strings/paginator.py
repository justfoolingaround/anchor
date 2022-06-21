def iter_contentaware_segments(
    string: str, max_length: int, *, separators=("\n", "\t", "\x10")
):
    """
    Iterate over string segments, splitting at separator characters, at their maximum length.
    """

    while string:
        separation_index = max(
            string.rfind(separator, 0, max_length) for separator in separators
        )

        if separation_index == -1:
            separation_index = max_length

        yield string[:separation_index]
        string = string[separation_index:].lstrip("".join(separators))
