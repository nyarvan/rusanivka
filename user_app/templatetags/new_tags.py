from django import template

register = template.Library()


@register.filter(name='split')
def split(value, splitter):
    """
    Splits a string into a list of substrings based on a given splitter.

    Args:
        value (str): The string to split.
        splitter (str): The delimiter used to split the string.

    Returns:
        list: List of substrings obtained by splitting the input string.
    """
    return value.split(splitter)


@register.filter(name='replace')
def replace(value, replace_item):
    """
    Replaces all occurrences of a substring with an empty string.

    Args:
        value (str): The input string.
        replace (str): The substring to replace.

    Returns:
        str: The input string with all occurrences of the substring replaced.
    """
    return value.replace(replace_item, '')


@register.filter(name="range")
def _range(_min, args=None):
    """
    Generates a range of integers.

    Args:
        _min (int): The starting value of the range.
        args (str, optional): Additional arguments. It can be either
        `_max` or `_max, _step`.

    Returns:
        range: A range of integers from `_min` to `_max`, with an optional
        step size `_step`.
    """
    _max, _step = None, None
    if args:
        if not isinstance(args, int):
            _max, _step = map(int, args.split(','))
        else:
            _max = args
    args = filter(None, (_min, _max, _step))
    return range(*args)
