from collections import namedtuple


# String representations for the bot's commands.
class Commands:
    PING = '!ping'
    INFO = '!info'
    DIE = '!die'


class ParamCommands:
    _schema = namedtuple('ParamsCommand', ['command', 'params'])
    SWITCH_LANG = _schema._make([
        'SWITCH_LANG', ['--en-us', '--ru-ru']
    ])
