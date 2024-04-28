from typing import Any, Callable, Dict, Awaitable

from aiogram import BaseMiddleware
from aiogram.dispatcher.flags import get_flag
from aiogram.types import TelegramObject, Message
from bot.database import users
from bot.handlers import start_register


class RegisterCheckMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[any]],
            event: Message,
            data: Dict[str, Any]
    ) -> Any:
        user = await users.get_user_by_id(event.from_user.id)
        if user:
            return await handler(event, data)
        register = get_flag(data, 'username')
        if not register:
            return await start_register(event, data['state'])
        return await handler(event, data)


