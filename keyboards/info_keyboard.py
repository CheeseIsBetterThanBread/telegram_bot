from aiogram.utils.keyboard import InlineKeyboardButton, InlineKeyboardMarkup


def build_info_keyboard() -> InlineKeyboardMarkup:
    button_tg_api = InlineKeyboardButton(
        text="Telegram bot api",
        url="https://core.telegram.org/bots/api#available-types"
    )
    button_requirements = InlineKeyboardButton(
        text="Requirements for project",
        url="https://docs.google.com/document/d/e/2PACX-1vQHz5CFdhcrpxaiL_G4Ju-1B6llUNSeFKvPSVRLIy7hqNXQ7m3xAAyKOqyhmZ2Os3rxUvVF84JZcbzU/pub"
    )
    button_source_code = InlineKeyboardButton(
        text="Source code for this bot",
        url="https://github.com/CheeseIsBetterThanBread/telegram_bot"
    )

    rows: list[list[InlineKeyboardButton]] = [
        [button_tg_api, button_requirements],
        [button_source_code]
    ]

    markup = InlineKeyboardMarkup(inline_keyboard = rows)
    return markup
