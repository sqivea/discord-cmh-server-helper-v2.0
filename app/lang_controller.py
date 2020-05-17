from pylocale import PyLocale


class LangController:
    translator = PyLocale(
        at='assets/translations',
        root='en-us',
        silent=False
    )
