from os import remove

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import FSInputFile, Message
from aiohttp import ClientSession
import vobject

from database import bot, contacts, convert_username_to_id, file_prefix
from database.contact import Contact

router = Router(name = __name__)


async def convert_to_vcard(contact: Contact) -> vobject.vCard:
    answer: vobject.vCard = vobject.vCard()
    answer.add('FN').value = contact.name
    answer.add('TEL').value = contact.telephone
    if contact.email:
        answer.add('EMAIL').value = contact.email
    return answer


async def is_identification(text: str) -> bool:
    try:
        string, number = text.split('_')
        number = int(number)
        return string == "contact" and number > 0
    except ValueError:
        return False


async def write_to_file(user_id: int, path: str) -> None:
    cards: list[vobject.vCard] = [await convert_to_vcard(contact) for contact in
                                  contacts[user_id]]
    with open(path, 'w') as file:
        for card in cards:
            file.write(card.serialize() + '\n')


async def find_id(user_id: int, aim: str) -> int:
    index: int = 0
    while index < len(contacts[user_id]):
        if contacts[user_id][index].contact_id == aim:
            break
        index += 1
    return index if index < len(contacts[user_id]) else -1


async def look_for_id(user_id: int,
                      contact_ids: list[str]) -> (list[int], list[str]):
    indexes: list[int] = []
    invalid: list[str] = []
    for contact in contact_ids:
        index: int = await find_id(user_id, contact)
        if index == -1:
            invalid.append(contact)
        else:
            indexes.append(index)
    return indexes, invalid


@router.message(Command('add_contact'))
async def add_contact_command(message: Message) -> None:
    user_id: int = message.from_user.id
    data: list[str] = message.text.split(' ')[1:]

    new_contact: Contact
    try:
        new_contact = Contact(data)
    except ValueError:
        await message.answer("Invalid input")
        return

    contacts[user_id].append(new_contact)
    await message.answer(f"Contact has been added:\n{new_contact.to_share()}")


@router.message(Command('import_contacts'))
async def import_contacts_command(message: Message) -> None:
    user_id: int = message.from_user.id
    document = message.document
    if not document:
        await message.answer("Provide a .vcf file")
        return

    file_id: str = document.file_id
    file_name: str = document.file_name
    if not file_name.endswith('.vcf'):
        await message.answer("File must have vcf extension")
        return

    file_info = await bot.get_file(file_id)
    file_url = f"{file_prefix}/{file_info.file_path}"
    async with ClientSession() as session:
        async with session.get(file_url) as response:
            file_content = await response.read()

    cards: list[vobject.vCard] = vobject.readComponents(
        file_content.decode('utf-8')
    )

    answer: str = "Imported contacts:\n"
    for card in cards:
        name: str = card.fn.value
        telephone: str = card.tel.value
        email: [str, None] = None
        if hasattr(card, 'email'):
            email = card.email.value

        data: list[str] = [telephone, name]
        if email:
            data.append(email)
        contact = Contact(data)

        contacts[user_id].append(contact)
        answer += str(contact) + '\n'

    await message.answer(answer)


@router.message(Command('view_contacts'))
async def view_contacts_command(message: Message) -> None:
    user_id: int = message.from_user.id
    contacts[user_id].sort()

    if not len(contacts[user_id]):
        await message.answer("You have no contacts saved")
        return

    response: str = ""
    for contact in contacts[user_id]:
        response += str(contact) + '\n'
    await message.answer(response)


@router.message(Command('export_contacts'))
async def export_contacts_command(message: Message) -> None:
    user_id: int = message.from_user.id
    contacts[user_id].sort()
    if not len(contacts[user_id]):
        await message.answer("There is nothing to export")
        return

    path: str = 'contacts.vcf'
    await write_to_file(user_id, path)

    await message.reply_document(
        document = FSInputFile(path = path, filename = 'contacts.vcf')
    )
    remove(path)


@router.message(Command('remove'))
async def remove_command(message: Message) -> None:
    user_id: int = message.from_user.id
    contact_id: str

    try:
        contact_id = message.text.split(' ')[1]
        if not (await is_identification(contact_id)):
            raise IndexError
    except IndexError:
        await message.answer("This id doesn't exist")
        return

    index: int = 0
    while index < len(contacts[user_id]):
        if contacts[user_id][index].contact_id == contact_id:
            break
        index += 1
    if index == len(contacts[user_id]):
        await message.answer("This id doesn't exist")
        return
    contacts[user_id].pop(index)

    await message.answer(f"Contact with id {contact_id} has been removed")


@router.message(Command('remove_all'))
async def remove_all_command(message: Message) -> None:
    contacts[message.from_user.id].clear()
    await message.answer("Your contacts have been removed")


@router.message(Command('send'))
async def send_command(message: Message) -> None:
    user: str = f"@{message.from_user.username}"
    user_id: int = message.from_user.id
    contact_ids: list[str]
    receiver: str
    data: list[str] = message.text.split(' ')[1:]

    try:
        receiver = data[0][1:]
    except IndexError:
        await message.answer("Specify the receiver")
        return

    contact_ids = data[1:]
    if not len(contact_ids):
        await message.answer("Specify the id")
        return

    indexes: list[int]
    invalid: list[str]
    indexes, invalid = await look_for_id(user_id, contact_ids)
    if not len(indexes):
        await message.answer("There is no valid id")
        return

    receiver_id: int
    try:
        receiver_id = convert_username_to_id[receiver]
    except KeyError:
        await message.answer(f"I don't know anyone named @{receiver}")
        return

    answer: str = f"User {user} sent you these contacts:\n"
    for index in indexes:
        answer += contacts[user_id][index].to_share() + '\n'
    await bot.send_message(receiver_id, text = answer)

    response: str = f"Contacts have been sent to @{receiver}\n"
    if len(invalid):
        response += "\nDidn't find contacts with ids:\n"
        for string in invalid:
            response += string + '\n'

    await message.answer(response)


@router.message(Command('send_all'))
async def send_all_command(message: Message) -> None:
    user_id: int = message.from_user.id
    user: str = message.from_user.username
    contacts[user_id].sort()
    if not len(contacts[user_id]):
        await message.answer("There is nothing to send")
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
        path: str = 'contacts.vcf'
        await write_to_file(user_id, path)

        await bot.send_document(
            receiver_id,
            document = FSInputFile(path = path, filename = 'contacts.vcf'),
            caption = f"From @{user}"
        )
        remove(path)
        await message.answer(f"Contacts have been sent to @{receiver}")
        return

    response: str = ""
    for contact in contacts[user_id]:
        response += contact.to_share() + '\n'

    await bot.send_message(
        receiver_id,
        text = f"User @{user} sent you their contact list:\n{response}"
    )
    await message.answer(f"Contacts have been sent to @{receiver}")
