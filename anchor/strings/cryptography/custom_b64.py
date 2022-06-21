import base64
import textwrap

BASE64_TABLE = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"


def cb64decode(data, *, table=BASE64_TABLE):
    return "".join(
        map(
            chr,
            base64.b64decode(
                (data + "=" * (len(data) % 4))
                .translate(str.maketrans(table, BASE64_TABLE))
                .encode()
            ),
        )
    )


def cb64encode(data, *, table=BASE64_TABLE):
    return "".join(
        table[int(segment.ljust(6, "0"), 2) if len(segment) < 6 else int(segment, 2)]
        for segment in textwrap.wrap(
            "".join(bin(ord(c)).lstrip("0b").rjust(8, "0") for c in data), 6
        )
    )
