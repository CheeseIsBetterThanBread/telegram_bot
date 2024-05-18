from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def build_help_event_keyboard() -> ReplyKeyboardMarkup:
    button_add_event = KeyboardButton(text = "add_event")
    button_import_events = KeyboardButton(text = "import_events")
    row_create_events: list[KeyboardButton] = [button_add_event,
                                               button_import_events]

    button_view_events = KeyboardButton(text = "view_events")
    button_export_events = KeyboardButton(text = "export_events")
    row_look_events: list[KeyboardButton] = [button_view_events,
                                             button_export_events]

    button_cancel = KeyboardButton(text = "cancel")
    button_cancel_old = KeyboardButton(text = "cancel_old")
    button_cancel_all = KeyboardButton(text = "cancel_all")
    row_cancel_events: list[KeyboardButton] = [button_cancel,
                                               button_cancel_old,
                                               button_cancel_all]

    button_share = KeyboardButton(text = "share")
    button_share_all = KeyboardButton(text = "share_all")
    row_share_events: list[KeyboardButton] = [button_share, button_share_all]

    button_back = KeyboardButton(text = "Back to /help")

    rows: list[list[KeyboardButton]] = [row_create_events,
                                        row_look_events,
                                        row_cancel_events,
                                        row_share_events,
                                        [button_back]]

    markup = ReplyKeyboardMarkup(keyboard = rows, resize_keyboard = True,
                                 one_time_keyboard = True)
    return markup
