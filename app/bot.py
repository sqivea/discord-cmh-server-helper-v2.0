from singletons import Singleton
from discord import Client as DiscordClient
from discord.message import Message


class CMHBot(DiscordClient, metaclass=Singleton):
    def __init__(self, **options) -> None:
        super().__init__(**options)

        @self.event
        async def on_message(message: Message) -> None:
            await self._process(message)

    async def _process(self, message: Message) -> None:
        if message.author == self.user:
            return
