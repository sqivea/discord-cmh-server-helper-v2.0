class WrongParamCommandError(Exception):
    """Raised when a parametrized command with a wrong param detected."""
    pass


class NoParamCommandError(Exception):
    """Raised when a parametrized command lacks a param."""
    pass
