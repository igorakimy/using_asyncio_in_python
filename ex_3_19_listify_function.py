from typing import Any, List


def listify(x: Any) -> List:
    """Try hard to convert x into a list"""
    if isinstance(x, (str, bytes)):
        return [x]
    try:
        return [_ for _ in x]
    except TypeError:
        return [x]
