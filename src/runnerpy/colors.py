NAMES = [
    'grey',
    'red',
    'green',
    'yellow',
    'blue',
    'magenta',
    'cyan',
    'white'
]


class ColorMeta(type):
    bold = '\033[1m'
    underline = '\033[4m'
    reset = '\033[0m'

    def __new__(cls, name, bases, attributes):
        colors = {}
        for i, name in enumerate(NAMES):
            colors[name] = '\033[{0}m'.format(str(30 + i))
            colors[f'bold_{name}'] = cls.bold + str(30 + i)
            colors[f'light_{name}'] = '\033[{0}m'.format(str(90 + i))
        attributes['colors'] = colors
        attributes.update(colors)
        return super().__new__(cls, name, bases, attributes)


class Color(metaclass=ColorMeta):

    @classmethod
    def fmt(cls, message, **context):
        context = {**context, **cls.colors}
        return message.format(**context)
