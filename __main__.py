import env  # noqa, used for loading the environment variables.

from os import getenv

from app import CMHBot as Bot


def main() -> None:
    Bot().run(getenv('BOT_TOKEN'))


if __name__ == '__main__':
    main()
