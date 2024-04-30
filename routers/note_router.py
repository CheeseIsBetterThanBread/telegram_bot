from os import remove

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import FSInputFile, Message
from aiohttp import ClientSession

from database import bot, convert_username_to_id, file_prefix, notes
from database.note import Note, separator

router = Router(name = __name__)


async def is_identification(text: str) -> bool:
    try:
        string, number = text.split('_')
        number = int(number)
        return string == "note" and number > 0
    except ValueError:
        return False


async def find_id(user_id: int, aim: str) -> int:
    index: int = 0
    while index < len(notes[user_id]):
        if notes[user_id][index].note_id == aim:
            break
        index += 1
    return index if index < len(notes[user_id]) else -1


async def look_for_id(user_id: int,
                      note_ids: list[str]) -> (list[int], list[str]):
    indexes: list[int] = []
    invalid: list[str] = []
    for note in note_ids:
        index: int = await find_id(user_id, note)
        if index == -1:
            invalid.append(note)
        else:
            indexes.append(index)
    return indexes, invalid


@router.message(Command('add_note'))
async def add_note_command(message: Message) -> None:
    user_id: int = message.from_user.id
    data: str = message.text[len('/add_note '):]

    new_note: Note
    try:
        new_note = Note(data)
    except ValueError:
        await message.answer("There is no note")
        return

    notes[user_id].append(new_note)
    await message.answer(f"Note with title {new_note.title} has been added")


@router.message(Command('import_note'))
async def import_note_command(message: Message) -> None:
    user_id: int = message.from_user.id
    document = message.document
    if not document:
        await message.answer("Provide a .txt file")
        return

    file_id: str = document.file_id
    file_name: str = document.file_name
    if not file_name.endswith('.txt'):
        await message.answer("File must have txt extension")
        return

    file_info = await bot.get_file(file_id)
    file_url = f"{file_prefix}/{file_info.file_path}"
    async with ClientSession() as session:
        async with session.get(file_url) as response:
            file_content = await response.read()

    temporary_file: str = "temporary.txt"
    with open(temporary_file, 'wb') as file:
        file.write(file_content)

    with open(temporary_file, 'r') as file:
        title: str = file.readline()
        data: str = file.read()  # you can't send large documents to bots
        new_note = Note(f"{title}{separator}{data}")
    remove(temporary_file)

    notes[user_id].append(new_note)
    await message.answer(f"Imported note:\n{new_note}")


@router.message(Command('view_notes'))
async def view_notes_command(message: Message) -> None:
    user_id: int = message.from_user.id
    notes[user_id].sort()

    if not len(notes[user_id]):
        await message.answer("You have no notes saved")
        return

    response: str = ""
    for note in notes[user_id]:
        response += str(note) + "\n\n"
    await message.answer(response)


@router.message(Command('export_notes'))
async def export_notes_command(message: Message) -> None:
    user_id: int = message.from_user.id
    notes[user_id].sort()
    if not len(notes[user_id]):
        await message.answer("There is nothing to export")
        return

    path: str = 'notes.txt'
    with open(path, 'w') as file:
        for note in notes[user_id]:
            file.write(note.to_share() + "\n\n")

    await message.reply_document(
        document = FSInputFile(path = path, filename = 'notes.txt')
    )
    remove(path)


@router.message(Command('delete'))
async def delete_command(message: Message) -> None:
    user_id: int = message.from_user.id
    note_id: str

    try:
        note_id = message.text.split(' ')[1]
        if not (await is_identification(note_id)):
            raise IndexError
    except IndexError:
        await message.answer("This id doesn't exist")
        return

    index: int = 0
    while index < len(notes[user_id]):
        if notes[user_id][index].note_id == note_id:
            break
        index += 1
    if index == len(notes[user_id]):
        await message.answer("This id doesn't exist")
        return
    notes[user_id].pop(index)

    await message.answer(f"Note with id {note_id} has been deleted")


@router.message(Command('delete_all'))
async def delete_all_command(message: Message) -> None:
    notes[message.from_user.id].clear()
    await message.answer("Your notes have been deleted")


@router.message(Command('drop'))
async def drop_command(message: Message) -> None:
    user: str = f"@{message.from_user.username}"
    user_id: int = message.from_user.id
    note_ids: list[str]
    receiver: str
    data: list[str] = message.text.split(' ')[1:]

    try:
        receiver = data[0][1:]
    except IndexError:
        await message.answer("Specify the receiver")
        return

    note_ids = data[1:]
    if not len(note_ids):
        await message.answer("Specify the id")
        return

    indexes: list[int]
    invalid: list[str]
    indexes, invalid = await look_for_id(user_id, note_ids)
    if not len(indexes):
        await message.answer("There is no valid id")
        return

    receiver_id: int
    try:
        receiver_id = convert_username_to_id[receiver]
    except KeyError:
        await message.answer(f"I don't know anyone named @{receiver}")
        return

    answer: str = f"User {user} sent you these notes:\n"
    for index in indexes:
        answer += notes[user_id][index].to_share() + '\n'
    await bot.send_message(receiver_id, text = answer)

    response: str = f"Notes have been sent to @{receiver}\n"
    if len(invalid):
        response += "\nDidn't find notes with ids:\n"
        for string in invalid:
            response += string + '\n'

    await message.answer(response)


@router.message(Command('drop_all'))
async def drop_all_command(message: Message) -> None:
    user_id: int = message.from_user.id
    user: str = message.from_user.username
    notes[user_id].sort()
    if not len(notes[user_id]):
        await message.answer("There is nothing to drop")
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
        path: str = 'notes.txt'
        with open(path, 'w') as file:
            for note in notes[user_id]:
                file.write(note.to_share() + "\n\n")

        await bot.send_document(
            receiver_id,
            document = FSInputFile(path = path, filename = 'notes.txt'),
            caption = f"From @{user}"
        )
        remove(path)

        await message.answer(f"Notes have been dropped to @{receiver}")
        return

    response: str = ""
    for note in notes[user_id]:
        response += note.to_share() + "\n\n"

    await bot.send_message(
        receiver_id,
        text = f"User @{user} sent you their notes:\n{response}"
    )
    await message.answer(f"Notes have been dropped to @{receiver}")
