from aiogram import F, Router
from aiogram.types import Message

from keyboards.help_contact_keyboard import build_help_contact_keyboard

router = Router(name = __name__)
username_format: str = "@<username>"
warning: str = (
    "Bot has to know the receiver "
    "(i.e. receiver has entered /start command before) "
    "otherwise it wont work\n"
)


@router.message(F.text == "Contact")
async def help_contact(message: Message) -> None:
    markup = build_help_contact_keyboard()
    await message.answer(
        text = "There you can see more information about contacts commands",
        reply_markup = markup
    )


@router.message(F.text == "add_contact")
async def help_add_contact(message: Message) -> None:
    answer: str = (
        f"This command allows you to add contact with syntax:\n"
        f"/add_contact <number> <name> <email>\n\n"
        f"Bot stores last ten digits of the number\n"
        f"Name can't contain @, otherwise bot will think it's an email\n"
        f"Email is optional. Has to contain @ for bot to detect it"
    )
    await message.answer(answer)


@router.message(F.text == "import_contacts")
async def help_import_contacts(message: Message) -> None:
    answer: str = (
        f"With this command you can import contacts from your .vcf file. "
        f"Syntax:\n"
        f"/import_contacts\n\n"
        f"You have to attach .vcf file to the message with command "
        f"in order for it to work"
    )
    await message.answer(answer)


@router.message(F.text == "view_contacts")
async def help_view_contacts(message: Message) -> None:
    answer: str = (
        f"This command will show your saved contacts. Syntax:\n"
        f"/view_contacts\n\n"
        f"Contacts are sorted by their names\n"
        f"It also shows contact id which you may need in other commands"
    )
    await message.answer(answer)


@router.message(F.text == "export_contacts")
async def help_export_contacts(message: Message) -> None:
    answer: str = (
        f"This command will export all of your contacts into .vcf file. "
        f"Syntax:\n"
        f"/export_contacts"
    )
    await message.answer(answer)


@router.message(F.text == "remove")
async def help_remove(message: Message) -> None:
    answer: str = (
        f"This command allows you to remove one of your contacts. Syntax:\n"
        f"/remove <contact identification>\n\n"
        f"You can see id of the contact with /view_contacts command"
    )
    await message.answer(answer)


@router.message(F.text == "remove_all")
async def help_remove_all(message: Message) -> None:
    answer: str = (
        f"This command will clear your contact list. Syntax:\n"
        f"/remove_all"
    )
    await message.answer(answer)


@router.message(F.text == "send")
async def help_send(message: Message) -> None:
    answer: str = (
        f"You can send your contacts to other telegram user with this command. "
        f"Syntax:\n"
        f"/send {username_format} <contact identifications>\n\n"
        f"You can see id of the contact with /view_contacts command\n{warning}"
    )
    await message.answer(answer)


@router.message(F.text == "send_all")
async def help_send_all(message: Message) -> None:
    answer: str = (
        f"You can send entire contact list to other telegram user using this. "
        f"Syntax:\n"
        f"/send_all {username_format} <format>\n\n{warning}"
        f"Bot supports two input values for format: 'file' and 'message'\n"
        f"'file' - contacts will be sent in a form of .vcf file\n"
        f"'message' - contacts will be sent as a message\n"
        f"Default value is 'file'"
    )
    await message.answer(answer)
