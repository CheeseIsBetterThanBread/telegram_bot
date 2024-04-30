from datetime import datetime
from os import remove

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import FSInputFile, Message
from aiohttp import ClientSession
from icalendar import Calendar, Event

from database import (
    add_notification,
    bot,
    cases,
    convert_username_to_id,
    file_prefix,
    offset,
    scheduler,
)
from database.case import Case
from database.time_and_date import Time

router = Router(name = __name__)


async def convert_to_datetime(current_time: Time) -> datetime:
    result: datetime = datetime(current_time.year, current_time.month,
                                current_time.day, current_time.hour,
                                current_time.minute)
    return result


async def is_identification(text: str) -> bool:
    try:
        string, number = text.split('_')
        number = int(number)
        return string == "identify" and number > 0
    except ValueError:
        return False


async def get_calendar(user_id: int) -> Calendar:
    user_calendar: Calendar = Calendar()
    for case in cases[user_id]:
        event: Event = Event()
        start: datetime = await convert_to_datetime(case.start)
        end: datetime = await convert_to_datetime(case.end)

        event.add('SUMMARY', case.description)
        event.add('DTSTART', start)
        event.add('DTEND', end)

        user_calendar.add_component(event)
    return user_calendar


async def get_message(user_id: int, to_share: bool = False) -> str:
    response: str = ""
    index: int = 1
    now = Time("")
    for case in cases[user_id]:
        response += f"Event #{index}"
        if case.end < now:
            response += " already passed\n"
        elif case.start < now:
            response += " in the process\n"
        else:
            response += '\n'
        response += str(case) if not to_share else case.to_share()
        response += '\n'
        index += 1
    return response


async def find_id(user_id: int, aim: str) -> int:
    index: int = 0
    while index < len(cases[user_id]):
        if cases[user_id][index].case_id == aim:
            break
        index += 1
    return index if index < len(cases[user_id]) else -1


async def look_for_id(user_id: int,
                      case_ids: list[str]) -> (list[int], list[str]):
    indexes: list[int] = []
    invalid: list[str] = []
    for case in case_ids:
        index: int = await find_id(user_id, case)
        if index == -1:
            invalid.append(case)
        else:
            indexes.append(index)
    return indexes, invalid


@router.message(Command('add_event'))
async def add_event_command(message: Message) -> None:
    user_id: int = message.from_user.id
    now = Time("")
    data: list[str] = message.text.split(' ')[1:]
    if not len(data):
        await message.answer("There is no such date")
        return

    try:
        case = Case(data)
    except ValueError:
        await message.answer("Invalid input")
        return

    delta: Time = offset[user_id]
    if case.start < now + delta:
        await message.answer("That time has already passed")
        return

    cases[user_id].append(case)
    notice: str = f"This event is starting soon: {case.description}"
    date: Time = case.start - delta - Time.delta(120)
    if date > Time(""):
        await add_notification(message.from_user.id,
                               notice, date, delta,
                               case.case_id)
    await message.answer(f"Set event with parameters:\n"
                         f"- beginning of the event: {case.start}\n"
                         f"- end of the event: {case.end}\n"
                         f"- note: {case.description}")


@router.message(Command('import_events'))
async def import_events_command(message: Message) -> None:
    user_id: int = message.from_user.id
    document = message.document
    if not document:
        await message.answer("Provide an .ics file")
        return

    file_id: str = document.file_id
    file_name: str = document.file_name
    if not file_name.endswith('.ics'):
        await message.answer("File must have ics extension")
        return

    file_info = await bot.get_file(file_id)
    file_url = f"{file_prefix}/{file_info.file_path}"
    async with ClientSession() as session:
        async with session.get(file_url) as response:
            file_content = await response.read()

    user_calendar: Calendar = Calendar.from_ical(file_content)
    answer: str = "Imported events:\n"
    index: int = 1
    for component in user_calendar.walk():
        if component.name == 'VEVENT':
            description: str = component.get('SUMMARY')
            datetime_start: datetime = component.get('DTSTART').dt
            datetime_end: datetime = component.get('DTEND').dt

            start: list[str] = datetime_start.strftime("%H:%M %d/%m/%Y").split()
            end: list[str] = datetime_end.strftime("%H:%M %d/%m/%Y").split()
            argument: list[str] = start + end
            argument.append(description)

            case = Case(argument)
            cases[user_id].append(case)

            answer += f"Event #{index}\n"
            answer += str(case) + '\n'
            index += 1
    await message.answer(answer)


@router.message(Command('view_events'))
async def view_events_command(message: Message) -> None:
    user_id: int = message.from_user.id
    cases[user_id].sort()

    if not len(cases[user_id]):
        await message.answer("You have no events yet")
        return

    response: str = await get_message(user_id)
    await message.answer(response)


@router.message(Command('export_events'))
async def export_events_command(message: Message) -> None:
    user_id: int = message.from_user.id
    cases[user_id].sort()
    if not len(cases[user_id]):
        await message.answer("There is nothing to export")
        return

    user_calendar: Calendar = await get_calendar(user_id)
    path: str = 'events.ics'
    with open(path, 'wb') as file:
        file.write(user_calendar.to_ical())

    await message.reply_document(
        document = FSInputFile(path = path, filename = 'events.ics')
    )
    remove(path)


@router.message(Command('cancel'))
async def cancel_command(message: Message) -> None:
    user_id: int = message.from_user.id
    case_id: str
    delta: Time = offset[user_id]
    border = Time("") + Time.delta(120) + delta

    try:
        case_id = message.text.split(' ')[1]
        if not (await is_identification(case_id)):
            raise IndexError
    except IndexError:
        await message.answer("This id doesn't exist")
        return

    index: int = 0
    while index < len(cases[user_id]):
        if cases[user_id][index].case_id == case_id:
            break
        index += 1
    if index == len(cases[user_id]):
        await message.answer("This id doesn't exist")
        return

    if border < cases[user_id][index].start:
        scheduler.remove_job(case_id)
    cases[user_id].pop(index)

    await message.answer(
        f"Event with id '{case_id}' has been canceled"
    )


@router.message(Command('cancel_old'))
async def cancel_old_command(message: Message) -> None:
    user_id: int = message.from_user.id
    delta: Time = offset[user_id]
    expired: list[Case] = []
    now = Time("") + delta

    for case in cases[user_id]:
        if case.end < now:
            expired.append(case)
    cases[user_id] = [case for case in cases[user_id] if case not in expired]

    await message.answer("Old events have been canceled")


@router.message(Command('cancel_all'))
async def cancel_all_command(message: Message) -> None:
    user_id: int = message.from_user.id
    delta: Time = offset[user_id]
    border: Time = Time("") + Time.delta(120) + delta

    for case in cases[user_id]:
        if case.start > border:
            scheduler.remove_job(case.case_id)
    cases[user_id].clear()

    await message.answer("Your events have been canceled")


@router.message(Command('share'))
async def share_command(message: Message) -> None:
    user: str = f"@{message.from_user.username}"
    user_id: int = message.from_user.id
    case_ids: list[str]
    receiver: str
    data: list[str] = message.text.split(' ')[1:]

    try:
        receiver = data[0][1:]
    except IndexError:
        await message.answer("Specify the receiver")
        return

    case_ids = data[1:]
    if not len(case_ids):
        await message.answer("Specify the id")
        return

    indexes: list[int]
    invalid: list[str]
    indexes, invalid = await look_for_id(user_id, case_ids)
    if not len(indexes):
        await message.answer("There is no valid id")
        return

    receiver_id: int
    try:
        receiver_id = convert_username_to_id[receiver]
    except KeyError:
        await message.answer(f"I don't know anyone named @{receiver}")
        return

    answer: str = f"User {user} sent you these events:\n"
    for index in indexes:
        answer += cases[user_id][index].to_share() + '\n'
    await bot.send_message(receiver_id, text = answer)

    response: str = f"Events have been sent to @{receiver}\n"
    if len(invalid):
        response += "\nDidn't find events with ids:\n"
        for string in invalid:
            response += string + '\n'

    await message.answer(response)


@router.message(Command('share_all'))
async def share_all_command(message: Message) -> None:
    user_id: int = message.from_user.id
    user: str = message.from_user.username
    cases[user_id].sort()
    if not len(cases[user_id]):
        await message.answer("There is nothing to share")
        return

    receiver: str
    structure: [None, str] = None
    data: list[str] = message.text.split(' ')[1:]

    if not len(data):
        await message.answer("Specify the receiver")
        return
    receiver = data[0][1:]
    if len(data) > 1:
        structure = data[1]
        if structure not in ["file", "message"]:
            await message.answer(
                f"Invalid format. I don't know what '{structure}' is"
            )
            return

    receiver_id: int
    try:
        receiver_id = convert_username_to_id[receiver]
    except KeyError:
        await message.answer(f"I don't know anyone named @{receiver}")
        return

    if not structure or structure == "file":
        user_calendar: Calendar = await get_calendar(user_id)
        path: str = 'events.ics'
        with open(path, 'wb') as file:
            file.write(user_calendar.to_ical())

        await bot.send_document(
            receiver_id,
            document = FSInputFile(path = path, filename = 'events.ics'),
            caption = f"From @{user}"
        )
        remove(path)
        await message.answer(f"Events have been sent to @{receiver}")
        return

    response: str = await get_message(user_id, True)
    await bot.send_message(
        receiver_id,
        text = f"User @{user} sent you their calendar:\n{response}"
    )
    await message.answer(f"Events have been sent to @{receiver}")
