from singletons import Singleton
from discord import Client as DiscordClient
from discord.message import Message

from .commands import Commands


class CMHBot(DiscordClient, metaclass=Singleton):
    def __init__(self, **options) -> None:
        super().__init__(**options)

        # Pairs of commands string representations
        # and bot's reactions for that commands.
        self._actions = {
            Commands.PING: self._on_ping,
            Commands.DIE: self._on_die
        }

        # Message handling decorator.
        @self.event
        async def on_message(message: Message) -> None:
            await self._process(message)

    async def _process(self, message: Message) -> None:
        if message.author == self.user:
            return

        action = self._actions.get(message.content)
        if not action:
            return

        await action(message)

    async def _on_ping(self, message: Message) -> None:
        await message.channel.send('Pong')

    async def _on_die(self, message: Message) -> None:
        await message.channel.send('Shutting down')
        await self.close()
