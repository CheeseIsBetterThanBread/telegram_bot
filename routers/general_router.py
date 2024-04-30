from datetime import datetime

import aiogram.types
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from database import (
    ADMIN,
    BANNED,
    add_notification,
    bot,
    cases,
    contacts,
    convert_username_to_id,
    notes,
    offset
)
from database.case import construct
from database.note import cut
from database.time_and_date import Time
from keyboards.help_keyboard import build_help_keyboard
from keyboards.info_keyboard import build_info_keyboard

router = Router(name = __name__)


@router.message(Command('start'))
async def start_command(message: Message) -> None:
    user: aiogram.types.User = message.from_user
    convert_username_to_id[user.username] = user.id
    cases[user.id] = []
    contacts[user.id] = []
    notes[user.id] = []
    offset[user.id] = Time.delta(0)
    await message.answer(f"Hello, {user.full_name}!\n"
                         f"I can help you organise your time\n"
                         f"To see what I can do, use /help command")

    warning: str = (
        f"Notice that for the bot to work properly, "
        f"you need to set your local time\n"
        f"You can do this by using /set_time command"
    )
    await message.answer(text = warning)


@router.message(Command('help'))
async def help_command(message: Message) -> None:
    general_answer: str
    general_answer = (
        f"With this bot you can:\n"
        f"- Get current time\n"
        f"- Set notifications for yourself\n"
        f"- Set events\n"
        f"- Import (export) events from (to) .ics files\n"
        f"- Cancel one or multiple events\n"
        f"- Share events with other telegram users\n"
        f"- Add contacts\n"
        f"- Import (export) contacts from (to) .vcf files\n"
        f"- Remove one or all of your contacts\n"
        f"- Send your contacts to other telegram users\n"
        f"- Create notes\n"
        f"- Import (export) notes from (to) .txt files\n"
        f"- Delete one or all of you notes\n"
        f"- Drop off your notes to other telegram users\n"
        f"\n"
        f"For more information click on the buttons"
    )
    markup = build_help_keyboard()
    await message.answer(general_answer, reply_markup = markup)


@router.message(Command('info'))
async def info_command(message: Message) -> None:
    markup = build_info_keyboard()
    await message.answer(
        text = "Useful links",
        reply_markup = markup
    )


@router.message(Command('time'))
async def time_command(message: Message) -> None:
    user_id: int = message.from_user.id
    now: Time = Time(datetime.now().strftime("%H:%M %d/%m/%Y"))
    await message.answer(str(now + offset[user_id]))


@router.message(Command('set_time'))
async def set_time_command(message: Message) -> None:
    user_id: int = message.from_user.id
    now: Time = Time("")
    actual_time: Time = Time("")
    data: list[str] = message.text.split(' ')[1:]
    if not len(data):
        await message.answer("Provide your time")
        return

    try:
        actual_time = Time(data[0] + " " + data[1])
    except:
        await message.answer("Provide a valid time")
        return

    offset[user_id] = actual_time - now
    answer: str = (
        f"Time has been set. "
        f"To see whether it is correct or not, use /time command"
    )
    await message.answer(answer)


@router.message(Command('notify'))
async def notify_command(message: Message) -> None:
    data: list[str] = message.text.split(' ')[1:]
    if not len(data):
        await message.answer("There is no date")
        return

    current_time: Time = Time("") + Time.delta(1)
    data, current_time = construct(data, current_time)

    delta: Time = offset[message.from_user.id]
    current_time -= delta

    notice: str = "There is your notice!"
    if len(data):
        notice = data[0]
        for index in range(1, len(data)):
            notice += " " + data[index]

    await add_notification(message.from_user.id, notice, current_time, delta)


@router.message(Command('suggest'))
async def suggest_command(message: Message) -> None:
    if message.from_user.username in BANNED:
        await message.answer("You can't use this command")
        return
    admin_id: int = convert_username_to_id[ADMIN]
    user: str = message.from_user.username

    suggestion: str = message.text[len('/suggest '):]
    suggestion = cut(suggestion)
    if not len(suggestion):
        await message.answer("You can't submit an empty suggestion")
        return

    to_admin: str = (
        f"User @{user} made a following suggestion:\n{suggestion}"
    )
    await bot.send_message(admin_id, to_admin)
    await message.answer("Suggestion has been sent")


@router.message(Command('ban'))
async def ban_command(message: Message) -> None:
    user: str = message.from_user.username
    if user != ADMIN:
        await message.answer("Permission denied")
        return

    client: str = message.text.split(' ')[1][1:]
    if client == ADMIN:
        await message.answer("You can't ban an admin")
        return

    BANNED.append(client)
    await message.answer(f"User @{client} has been banned")


@router.message(Command('unban'))
async def unban_command(message: Message) -> None:
    user: str = message.from_user.username
    if user != ADMIN:
        await message.answer("Permission denied")
        return

    client: str = message.text.split(' ')[1][1:]
    if client in BANNED:
        BANNED.remove(client)
        await message.answer(f"User @{client} has been unbanned")
        return
    await message.answer(f"User @{client} is not banned")


@router.message(Command('view_banned'))
async def view_banned_command(message: Message) -> None:
    user: str = message.from_user.username
    if user != ADMIN:
        await message.answer("Permission denied")
        return

    response: str = ""
    index: int = 1
    for username in BANNED:
        response += f"{index}. @{username}\n"

    if response:
        await message.answer(response)
    else:
        await message.answer("No one is banned")


@router.message()
async def general_response_command(message: Message) -> None:
    await message.answer("Sorry, i don't know this command")
