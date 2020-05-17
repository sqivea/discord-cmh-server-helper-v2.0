from .lang_controller import LangController


class classProperty(property):
    """Decorates properties of classes,
       which must be accessible explicitly.
    """

    def __get__(self, cls, owner):
        return self.fget.__get__(None, owner)()


# String representations for replies.
class Replies:
    @classProperty
    @classmethod
    def ON_PING(cls) -> str:
        return '`{}`'.format(LangController.translator['ON_PING'])

    @classProperty
    @classmethod
    def ON_DIE(cls) -> str:
        return '`{}`'.format(LangController.translator['ON_DIE'])

    @classProperty
    @classmethod
    def ON_INFO(cls) -> str:
        return '`{}`'.format(LangController.translator['ON_INFO'])

    @classProperty
    @classmethod
    def ON_WRONG_PARAM(cls) -> str:
        return '`{}`'.format(LangController.translator['ON_WRONG_PARAM'])
