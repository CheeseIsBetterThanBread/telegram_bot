from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def build_help_keyboard() -> ReplyKeyboardMarkup:
    button_time = KeyboardButton(text = "time")
    button_set_time = KeyboardButton(text = "set_time")
    button_notify = KeyboardButton(text = "notify")
    button_suggest = KeyboardButton(text = "suggest")
    row_basic: list[KeyboardButton] = [button_time,
                                       button_set_time,
                                       button_notify,
                                       button_suggest]

    button_redirect_contact = KeyboardButton(text = "Contact")
    button_redirect_event = KeyboardButton(text = "Event")
    button_redirect_note = KeyboardButton(text = "Note")
    row_redirect: list[KeyboardButton] = [button_redirect_contact,
                                          button_redirect_event,
                                          button_redirect_note]

    rows: list[list[KeyboardButton]] = [row_basic, row_redirect]

    markup = ReplyKeyboardMarkup(keyboard = rows, resize_keyboard = True,
                                 one_time_keyboard = True)
    return markup
