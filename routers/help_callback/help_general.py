from aiogram import F, Router
from aiogram.types import Message

from keyboards.help_keyboard import build_help_keyboard

router = Router(name = __name__)
time_format: str = "<hours>:<minutes> <day>/<month>/<year>"


@router.message(F.text == "time")
async def help_time(message: Message) -> None:
    answer: str = (
        f"You can get current time using command:\n"
        f"/time\n\n"
        f"Result will be in a format:\n{time_format}"
    )
    await message.answer(answer)


@router.message(F.text == "set_time")
async def help_set_time(message: Message) -> None:
    answer: str = (
        f"You can synchronize your local time with the one, "
        f"that bot uses, bva this command. Syntax:\n"
        f"/set_time {time_format}"
    )
    await message.answer(answer)


@router.message(F.text == "notify")
async def help_notify(message: Message) -> None:
    answer: str = (
        f"With this function you can create notification using syntax:\n"
        f"/notify <time> <text>\n\n"
        f"Here time should be in a format:\n{time_format}\n"
        f"If you specify only time or only date of notification, "
        f"other parameter will be taken from current time\n"
        f"Text parameter is optional"
    )
    await message.answer(answer)


@router.message(F.text == "suggest")
async def help_suggest(message: Message) -> None:
    answer: str = (
        f"You can suggest a change, that this bot might need with command:\n"
        f"/suggest <your proposal>\n\n"
        f"Developers will see, whose proposal it is and "
        f"we reserve the right to revoke your access to this command "
        f"if you spam meaningless suggestions"
    )
    await message.answer(answer)


@router.message(F.text == "Back to /help")
async def return_to_help_keyboard(message: Message) -> None:
    markup = build_help_keyboard()
    await message.answer("Returning to /help", reply_markup = markup)
