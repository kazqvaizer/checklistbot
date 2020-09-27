_registry = {
    "general_help": {
        "en": (
            "Yes, this is an another check list bot. But this one is the simplest:\n"
            "* Add items by sending text messages\n"
            "* Strike out items by sending their index\n"
            "* If you check off all items - your list would be cleaned automatically\n"
            "* Send /start to clean up previous list and start a new one\n"
            "* Send /toggle to enable or disable bot (useful in chat groups)"
        ),
        "ru": (
            "Да, это очередной бот для составления списка дел. Но он очень простой:\n"
            "* Добавляйте позиции в список просто отправляя текстовые сообщения\n"
            "* Вычеркивайте позиции, отправляя их номер\n"
            "* Вычеркните все позиции, чтобы закончить список и начать новый\n"
            "* Отправьте /start чтобы стереть имеющийся список и начать его заново\n"
            "* Отправьте /toggle чтобы включить или выключить бота (удобно в группах)"
        ),
    },
    "to_start_help": {
        "en": "To start a new to-do list, please, send me few text lines.",
        "ru": "Чтобы начать новый список, пожалуйста, скиньте мне несколько строк.",
    },
    "enabled": {
        "en": "Enabled! Send /toggle again to disable.",
        "ru": "Включен! Отправьте /toggle чтобы выключить.",
    },
    "disabled": {
        "en": "Disabled! All messages will be ignored. Send /toggle again to enable.",
        "ru": (
            "Выключен! Все сообщения будут проигнорированы. "
            "Отправьте /toggle чтобы включить."
        ),
    },
    "to_check_off_help": {
        "en": "To check off the item simply send me its index number.",
        "ru": "Чтобы вычеркнуть строчку просто пришлите мне её номер.",
    },
    "no_items_to_check_off": {
        "en": "It seems that you have no items in your list to check off.",
        "ru": "Кажется, что в вашем списке нечего вычеркнуть.",
    },
    "congrats": {
        "en": "Congratulations! You have been finished you to-do list!",
        "ru": "Поздравляю! Вы завершили свой список дел!",
    },
    "no_index": {
        "en": "Sorry, this index was not found.",
        "ru": "Извините, но такой индекс не найден.",
    },
    "deleted": {
        "en": "Your previous list has just been deleted!",
        "ru": "Ваш предыдущий список дел был удален!",
    },
}


class CommonMessages:
    """Simple registry with all common replies."""

    def __init__(self, language_code: str):
        self.language_code = language_code

    def get_message(self, slug: str) -> str:
        messages = _registry[slug]
        return messages.get(self.language_code, messages["en"])
