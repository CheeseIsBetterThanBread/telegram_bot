from aiogram import F, Router
from aiogram.types import Message

from keyboards.help_event_keyboard import build_help_event_keyboard

router = Router(name = __name__)
time_format: str = "<hours>:<minutes> <day>/<month>/<year>"
username_format: str = "@<username>"
warning: str = (
    "Bot has to know the receiver "
    "(i.e. receiver has entered /start command before) "
    "otherwise it wont work\n"
)


@router.message(F.text == "Event")
async def help_event(message: Message) -> None:
    markup = build_help_event_keyboard()
    await message.answer(
        text = "There you can see more information about event commands",
        reply_markup = markup
    )


@router.message(F.text == "add_event")
async def help_add_event(message: Message) -> None:
    answer: str = (
        f"This function allows you to set up an event in your calendar\n"
        f"To do this, use following command:\n"
        f"/add_event <time of the start> <time of the end> <description>\n\n"
        f"Both times should be in format:\n{time_format}\n"
        f"Missing arguments for time of the start are taken from current time, "
        f"and for time of the end - from time of the start."
        f"You can't set an event, "
        f"that starts before time the message was sent\n"
        f"If your event starts at least two hours from now, then you will "
        f"receive notification two hours prior to the start of your event\n"
        f"Description is optional"
    )
    await message.answer(answer)


@router.message(F.text == "import_events")
async def help_import_events(message: Message) -> None:
    answer: str = (
        f"This command will import events from .ics file to this bot. Syntax:\n"
        f"/import_events\n\n"
        f"You have to attach .ics file to the message with command "
        f"in order for it to work\n"
    )
    await message.answer(answer)


@router.message(F.text == "view_events")
async def help_view_events(message: Message) -> None:
    answer: str = (
        f"This function will show you all scheduled events using command:\n"
        f"/view_events\n\n"
        f"Events are sorted by times of their starts\n"
        f"It also shows event id, which you may need to use other commands"
    )
    await message.answer(answer)


@router.message(F.text == "export_events")
async def help_export_events(message: Message) -> None:
    answer: str = (
        f"This function will export all your events "
        f"(including those, that have already passed) into .ics file\n"
        f"You can achieve this with command:\n"
        f"/export_events"
    )
    await message.answer(answer)


@router.message(F.text == "cancel")
async def help_cancel(message: Message) -> None:
    answer: str = (
        f"This function will cancel one event in your schedule."
        f"It is invoked by command:\n"
        f"/cancel <event identification>\n\n"
        f"You can see id of the event with /view_events command"
    )
    await message.answer(answer)


@router.message(F.text == "cancel_old")
async def help_cancel_old(message: Message) -> None:
    answer: str = (
        f"This function will cancel all finished events with command:\n"
        f"/cancel_old"
    )
    await message.answer(answer)


@router.message(F.text == "cancel_all")
async def help_cancel_all(message: Message) -> None:
    answer: str = (
        f"This function will clear your schedule after using command:\n"
        f"/cancel_all"
    )
    await message.answer(answer)


@router.message(F.text == "share")
async def help_share(message: Message) -> None:
    answer: str = (
        f"You can send your events to other telegram user with this command. "
        f"Syntax:\n"
        f"/share {username_format} <event identifications>\n\n"
        f"You can see id of the event with /view_events command\n{warning}"
    )
    await message.answer(answer)


@router.message(F.text == "share_all")
async def help_share_all(message: Message) -> None:
    answer: str = (
        f"You can share entire schedule with other telegram user using this. "
        f"Syntax:\n"
        f"/share_all {username_format} <format>\n\n{warning}"
        f"Bot supports two input values for format: 'file' and 'message'\n"
        f"'file' - events will be sent in a form of .ics file\n"
        f"'message' - events will be sent as a message\n"
        f"Default value is 'file'"
    )
    await message.answer(answer)
