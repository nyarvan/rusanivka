from django import template

register = template.Library()

@register.filter(name='split')
def split(value, splitter):
    return value.split(splitter)

@register.filter(name='replace')
def replace(value, replace):
    return value.replace(replace, '')

@register.filter(name="range")
def _range(_min, args=None):
    _max, _step = None, None
    if args:
        if not isinstance(args, int):
            _max, _step = map(int, args.split(','))
        else:
            _max = args
    args = filter(None, (_min, _max, _step))
    return range(*args)
