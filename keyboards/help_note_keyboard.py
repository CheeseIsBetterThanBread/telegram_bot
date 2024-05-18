from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def build_help_note_keyboard() -> ReplyKeyboardMarkup:
    button_add_note = KeyboardButton(text = "add_note")
    button_import_note = KeyboardButton(text = "import_note")
    row_create_note: list[KeyboardButton] = [button_add_note,
                                             button_import_note]

    button_view_notes = KeyboardButton(text = "view_notes")
    button_export_notes = KeyboardButton(text = "export_notes")
    row_look_notes: list[KeyboardButton] = [button_view_notes,
                                            button_export_notes]

    button_delete = KeyboardButton(text = "delete")
    button_delete_all = KeyboardButton(text = "delete_all")
    row_delete_notes: list[KeyboardButton] = [button_delete, button_delete_all]

    button_drop = KeyboardButton(text = "drop")
    button_drop_all = KeyboardButton(text = "drop_all")
    row_drop_notes: list[KeyboardButton] = [button_drop, button_drop_all]

    button_back = KeyboardButton(text = "Back to /help")

    rows: list[list[KeyboardButton]] = [row_create_note,
                                        row_look_notes,
                                        row_delete_notes,
                                        row_drop_notes,
                                        [button_back]]

    markup = ReplyKeyboardMarkup(keyboard = rows, resize_keyboard = True,
                                 one_time_keyboard = True)
    return markup
