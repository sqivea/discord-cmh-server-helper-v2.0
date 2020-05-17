from typing import List, Callable

from singletons import Singleton
from discord import Client as DiscordClient
from discord.message import Message

from .commands import Commands, ParamCommands
from .errors import WrongParamCommandError, NoParamCommandError
from .replies import Replies

from .lang_controller import LangController


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
        DELETE_MSGS = ParamCommands.DELETE_MSGS
        self._param_actions = {
            SWITCH_LANG: lambda command: self._on_switch(command),
            DELETE_MSGS: lambda command: self._on_delete(command)
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
            try:
                action = await self._find_param_command(content)
            except WrongParamCommandError as ex:
                await message.channel.send(str(ex))
            except NoParamCommandError as ex:
                await message.channel.send(str(ex))
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

    async def _on_switch(self, message: Message) -> None:
        _, locale_param = self._get_processed_content(message.content).split()
        switched_locale = locale_param.replace('--', '')
        LangController.translator.switch(switched_locale)
        await message.channel.send(
            '{} `{}`'.format(Replies.ON_CURRENT_LOCALE, switched_locale)
        )

    async def _on_delete(self, message: Message) -> None:
        command, param = message.content.split()
        limit = {
            '--10': 10,
            '--50': 50,
            '--100': 100,
            '--all': None
        }[param]
        to_delete: List[Message] = []
        counter = 0
        async for old_one in message.channel.history(limit=None):
            if limit and counter == limit:
                break
            elif old_one.author.id == message.author.id:
                to_delete.append(old_one)
                counter += 1

        await message.channel.delete_messages(to_delete)

    async def _find_param_command(self, message: str) -> Callable:
        try:
            command, param = message.split()
        except ValueError:
            param_action = await self._get_param_action(message)
            if not param_action:
                return None
            else:
                # Reraise the exception with additional info.
                raise NoParamCommandError(
                    '{}'.format(Replies.ON_PARAM_NOT_PRESENT)
                )

        param_action = await self._get_param_action(command)
        if not param_action:
            return None
        else:
            await self._check_param(command, param)
            return param_action

    async def _get_param_action(self, command: str) -> Callable:
        return dict([
            (command_object.command, reaction)
            for command_object, reaction in self._param_actions.items()
        ]).get(command)

    async def _check_param(self, command: str, param: str) -> None:
        named_param_actions = dict([
            (command_object.command, command_object.params)
            for command_object in self._param_actions.keys()
        ])
        if param not in named_param_actions[command]:
            raise WrongParamCommandError(
                '{}: `{}`'.format(Replies.ON_WRONG_PARAM, param)
            )
