import asyncio

from aiogram import Dispatcher
from aiogram.types import BotCommand

from database import bot, scheduler
from routers import router as main_router


dp = Dispatcher()
dp.include_routers(main_router)

commands = [
    BotCommand(command = 'help', description = "Get help"),
    BotCommand(command = 'time', description = "Get current time"),
    BotCommand(command = 'set_time', description = "Set local time"),
    BotCommand(command = 'notify', description = "Set notification"),
    BotCommand(command = 'suggest', description = "Suggest a change"),

    BotCommand(command = 'add_event', description = "Add new event"),
    BotCommand(command = 'import_events',
               description = "Import events from .ics file"),
    BotCommand(command = 'view_events', description = "See current events"),
    BotCommand(command = 'export_events',
               description = "Export events into .ics file"),

    BotCommand(command = 'cancel', description = "Cancel one event"),
    BotCommand(command = 'cancel_old', description = "Cancel old events"),
    BotCommand(command = 'cancel_all', description = "Cancel all events"),

    BotCommand(command = 'share', description = "Share one event"),
    BotCommand(command = 'share_all', description = "Share all events"),

    BotCommand(command = 'add_contact', description = "Add new contact"),
    BotCommand(command = 'import_contacts',
               description = "Import contacts from .vcf file"),
    BotCommand(command = 'view_contacts', description = "See saved contacts"),
    BotCommand(command = 'export_contacts',
               description = "Export contacts into .vcf file"),

    BotCommand(command = 'remove', description = "Remove one contact"),
    BotCommand(command = 'remove_all', description = "Remove all contacts"),

    BotCommand(command = 'send', description = "Send one contact"),
    BotCommand(command = 'send_all', description = "Send all contacts"),

    BotCommand(command = 'add_note', description = "Add new note"),
    BotCommand(command = 'import_note',
               description = "Import note from .txt file"),
    BotCommand(command = 'view_notes', description = "See saved notes"),
    BotCommand(command = 'export_notes',
               description = "Export notes into .txt file"),

    BotCommand(command = 'delete', description = "Delete one note"),
    BotCommand(command = 'delete_all', description = "Delete all notes"),

    BotCommand(command = 'drop', description = "Drop one contact"),
    BotCommand(command = 'drop_all', description = "Drop all contacts"),
]


async def main() -> None:
    scheduler.start()
    await bot.set_my_commands(commands)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
