_registry = {
    "to_start_help": {
        "en": "To start a new to-do list, please, send me few text lines.",
        "ru": "Чтобы начать новый список, пожалуйста, скиньте мне несколько строк.",
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
        "en": "Sorry I cannot find item with this index.",
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
