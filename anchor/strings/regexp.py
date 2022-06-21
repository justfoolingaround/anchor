import re


URL_HOST_REGEX = re.compile(
    r"^(?P<scheme_prefix>(?P<scheme>.*?):.*?//)?(?P<basic_authorization>[a-zA-Z0-9-]+?:[a-zA-Z0-9-]+?@)?(?P<host>(?:[a-zA-Z0-9-]+?\.)+[a-zA-Z0-9-]+(?P<port>:\d+)?)(?P<path>(?:/[^/?&#]*)*)?"
)


def _get_segment(segment, retain, replacement_segment, force_presense, escape_segment):

    if retain and segment:
        if escape_segment:
            regex_segment = f"(?:{re.escape(segment)})"
        else:
            regex_segment = f"(?:{segment})"
    else:
        regex_segment = replacement_segment

    if not force_presense:
        regex_segment += "?"

    return regex_segment


def regexify_url(
    url: str,
    flags=re.IGNORECASE,
    *,
    extra: str = "",
    extra_re: str = "",
    match_subdomains: bool = True,
    retain_scheme: bool = True,
    retain_basic_authorization: bool = True,
    retain_path: bool = True,
    force_scheme_presence: bool = False,
    force_basic_authorization_presence: bool = False,
    force_path_presence: bool = False,
    strict: bool = False,
) -> re.Pattern:
    """
    Automatically convert a URL to a regex pattern.


    :param url: The URL to convert.
    :param flags: The regex flags to use.
    :param extra: Extra non-regex pattern to match.
    :param extra_re: Extra regex pattern to match.
    :param match_subdomains: Whether to match subdomains.
    :param retain_scheme: Whether to retain the scheme.
    :param retain_basic_authorization: Whether to retain the basic authorization.
    :param retain_path: Whether to retain the path.
    :param force_scheme_presence: Whether to force the scheme to be present.
    :param force_basic_authorization_presence: Whether to force the basic authorization to be present.
    :param force_path_presence: Whether to force the path to be present.
    :param strict: Whether to use strict mode.
    :return: The regex pattern.
    """

    regex_match = URL_HOST_REGEX.match(url)

    if not regex_match:
        raise ValueError(f"Could not resolve URL from {url!r}")

    url_segments = regex_match.groupdict()

    host_regex_segment = re.escape(url_segments["host"])

    if match_subdomains:
        host_regex_segment = r"(?:[a-zA-Z0-9-]+?\.)*" + host_regex_segment

    if url_segments["port"]:
        host_regex_segment += url_segments["port"]
    else:
        host_regex_segment += "(?::\d+)?"

    full_re = (
        _get_segment(
            url_segments.get("scheme_prefix"),
            retain_scheme,
            r"(?:.*?:.*?//)",
            force_scheme_presence,
            True,
        )
        + _get_segment(
            url_segments.get("basic_authorization"),
            retain_basic_authorization,
            r"(?:[a-zA-Z0-9-]+?:[a-zA-Z0-9-]+?@)",
            force_basic_authorization_presence,
            True,
        )
        + host_regex_segment
        + _get_segment(
            url_segments.get("path"),
            retain_path,
            "",
            force_path_presence,
            True,
        )
        + re.escape(extra)
        + extra_re
    )

    if strict:
        full_re = "^{}$".format(full_re)

    return re.compile(full_re, flags=flags)


if __name__ == "__main__":

    url = "abc.xyz/abc/"

    regex = regexify_url(url)

    assert regex.fullmatch("abc.xyz")
    assert regex.fullmatch("abc.xyz/abc/")
    assert regex.fullmatch("https://abc.xyz/abc/")
    assert regex.fullmatch("https://username:password@abc.xyz/abc/")
    assert regex.fullmatch("https://username:password@abc.xyz:8080/abc/")
