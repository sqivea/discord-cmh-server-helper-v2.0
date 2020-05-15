from singletons import Singleton
from discord import Client as DiscordClient


class CMHBot(DiscordClient, metaclass=Singleton):
    pass
