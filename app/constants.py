from .lang_controller import LangController


# String representations for replies.
class Replies:
    ON_PING = '`{}`'.format(LangController.translator['ON_PING'])
    ON_DIE = '`{}`'.format(LangController.translator['ON_DIE'])
    ON_INFO = '`{}`'.format(LangController.translator['ON_INFO'])
