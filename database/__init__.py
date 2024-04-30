from os import environ

from aiogram import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from .case import Case
from .contact import Contact
from .note import Note
from .time_and_date import Time


API_TOKEN: str = environ['API_TOKEN']
ADMIN: str = environ['ADMIN']
BANNED: list[str] = []

file_prefix: str = f"https://api.telegram.org/file/bot{API_TOKEN}"
bot: Bot = Bot(token = API_TOKEN)
scheduler: AsyncIOScheduler = AsyncIOScheduler()

convert_username_to_id: dict[str, int] = {}

cases: dict[int, list[Case]] = {}
contacts: dict[int, list[Contact]] = {}
notes: dict[int, list[Note]] = {}
offset: dict[int, Time] = {}


async def send_message(chat_id: int, message: str) -> None:
    await bot.send_message(chat_id = chat_id, text = message)


async def add_notification(chat_id: int, message: str, date: Time, delta: Time,
                           event_id: str | None = None) -> None:
    if event_id:
        scheduler.add_job(send_message, 'date', run_date = date.refactored(),
                          args = [chat_id, message], id = event_id)
    else:
        scheduler.add_job(send_message, 'date', run_date = date.refactored(),
                          args = [chat_id, message])
    await bot.send_message(chat_id = chat_id,
                           text = f"Notification is set at {date + delta}")
