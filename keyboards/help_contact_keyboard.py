from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def build_help_contact_keyboard() -> ReplyKeyboardMarkup:
    button_add_contact = KeyboardButton(text = "add_contact")
    button_import_contacts = KeyboardButton(text = "import_contacts")
    row_create_contacts: list[KeyboardButton] = [button_add_contact,
                                                 button_import_contacts]

    button_view_contacts = KeyboardButton(text = "view_contacts")
    button_export_contacts = KeyboardButton(text = "export_contacts")
    row_look_contacts: list[KeyboardButton] = [button_view_contacts,
                                               button_export_contacts]

    button_remove = KeyboardButton(text = "remove")
    button_remove_all = KeyboardButton(text = "remove_all")
    row_remove_contacts: list[KeyboardButton] = [button_remove,
                                                 button_remove_all]

    button_send = KeyboardButton(text = "send")
    button_send_all = KeyboardButton(text = "send_all")
    row_send_contacts: list[KeyboardButton] = [button_send, button_send_all]

    button_back = KeyboardButton(text = "Back to /help")

    rows: list[list[KeyboardButton]] = [row_create_contacts,
                                        row_look_contacts,
                                        row_remove_contacts,
                                        row_send_contacts,
                                        [button_back]]

    markup = ReplyKeyboardMarkup(keyboard = rows, resize_keyboard = True,
                                 one_time_keyboard = True)
    return markup
