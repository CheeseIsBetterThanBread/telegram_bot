from aiogram import F, Router
from aiogram.types import Message

from keyboards.help_note_keyboard import build_help_note_keyboard

router = Router(name = __name__)
username_format: str = "@<username>"
warning: str = (
    "Bot has to know the receiver "
    "(i.e. receiver has entered /start command before) "
    "otherwise it wont work\n"
)


@router.message(F.text == "Note")
async def help_note(message: Message) -> None:
    markup = build_help_note_keyboard()
    await message.answer(
        text = "There you can see more information about note commands",
        reply_markup = markup
    )


@router.message(F.text == "add_note")
async def help_add_note(message: Message) -> None:
    answer: str = (
        f"This command allows you to add note with syntax:\n"
        f"/add_note <title> <separator> <text>\n\n"
        f"Title is optional. By default it is 'Untitled'\n"
        f"Use !# symbol to separate title from text "
    )
    await message.answer(answer)


@router.message(F.text == "import_note")
async def help_import_note(message: Message) -> None:
    answer: str = (
        f"With this command you can import note from your .txt file. "
        f"Notice, that bot will think that file contains only one note. "
        f"Syntax:\n"
        f"/import_note\n\n"
        f"You have to attach .vcf file to the message with command "
        f"in order for it to work\n"
        f"Bot will expect first line of the file to be a title"
    )
    await message.answer(answer)


@router.message(F.text == "view_notes")
async def help_view_notes(message: Message) -> None:
    answer: str = (
        f"This command will show your saved notes. Syntax:\n"
        f"/view_notes\n\n"
        f"Notes are sorted by their titles\n"
        f"It also shows note id which you may need in other commands"
    )
    await message.answer(answer)


@router.message(F.text == "export_notes")
async def help_export_notes(message: Message) -> None:
    answer: str = (
        f"This command will export all of your notes into .txt file. "
        f"Syntax:\n"
        f"/export_notes"
    )
    await message.answer(answer)


@router.message(F.text == "delete")
async def help_delete(message: Message) -> None:
    answer: str = (
        f"This command allows you to delete one of your notes. Syntax:\n"
        f"/delete <note identification>\n\n"
        f"You can see id of the note with /view_notes command"
    )
    await message.answer(answer)


@router.message(F.text == "delete_all")
async def help_delete_all(message: Message) -> None:
    answer: str = (
        f"This command will clear your notes list. Syntax:\n"
        f"/delete_all"
    )
    await message.answer(answer)


@router.message(F.text == "drop")
async def help_drop(message: Message) -> None:
    answer: str = (
        f"You can send your notes to other telegram user with this command. "
        f"Syntax:\n"
        f"/drop {username_format} <note identifications>\n\n"
        f"You can see id of the note with /view_contacts command\n{warning}"
    )
    await message.answer(answer)


@router.message(F.text == "drop_all")
async def help_drop_all(message: Message) -> None:
    answer: str = (
        f"You can send entire list of notes to other telegram user using this. "
        f"Syntax:\n"
        f"/drop_all {username_format} <format>\n\n{warning}"
        f"Bot supports two input values for format: 'file' and 'message'\n"
        f"'file' - contacts will be sent in a form of .vcf file\n"
        f"'message' - contacts will be sent as a message\n"
        f"Default value is 'file'"
    )
    await message.answer(answer)
