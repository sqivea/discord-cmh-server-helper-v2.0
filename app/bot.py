from typing import Callable

from singletons import Singleton
from discord import Client as DiscordClient
from discord.message import Message

from .commands import Commands, ParamCommands
from .errors import WrongParamCommandError
from .constants import Replies


class CMHBot(DiscordClient, metaclass=Singleton):
    def __init__(self, **options) -> None:
        super().__init__(**options)

        # Pairs of commands string representations
        # and bot's explicit reactions for those commands.
        self._actions = {
            Commands.PING: self._on_ping,
            Commands.INFO: self._on_info,
            Commands.DIE: self._on_die
        }

        # Pairs of commands strings representations
        # and their parameters which will then be processed.
        SWITCH_LANG = ParamCommands.SWITCH_LANG
        self._param_actions = {
            SWITCH_LANG: lambda command: self._on_switch(command)
        }

        # Message handling decorator.
        @self.event
        async def on_message(message: Message) -> None:
            await self._process(message)

    async def _process(self, message: Message) -> None:
        # Do not reply for own messages.
        if message.author == self.user:
            return

        # Command matching.
        content = self._get_processed_content(message.content)
        action = self._actions.get(content)
        if not action:
            return

        # If the message represents a command, execute it.
        await action(message)

    def _get_processed_content(self, message: str) -> str:
        return ' '.join(message.split())

    async def _on_ping(self, message: Message) -> None:
        await message.channel.send(Replies.ON_PING)

    async def _on_info(self, message: Message) -> None:
        await message.channel.send(Replies.ON_INFO)

    async def _on_die(self, message: Message) -> None:
        await message.channel.send(Replies.ON_DIE)
        await self.close()

    async def _find_param_command(self, message: Message) -> Callable:
        command, param = message.split()
        param_action = dict([
            (command_object.command, reaction)
            for command_object, reaction in self._param_actions.items()
        ]).get(command)
        if not param_action:
            return None
        else:
            self._check_param(command, param)
            return param_action

    async def _check_param(self, command: str, param: str) -> None:
        named_param_actions = dict([
            (command_object.command, command_object.params)
            for command_object in self._param_actions.keys()
        ])
        if param not in named_param_actions[command].params:
            raise WrongParamCommandError()

    async def _on_switch(self, message: Message) -> None:
        pass
