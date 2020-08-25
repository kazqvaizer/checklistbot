# Simple registry of all possible replies

registry = {
    "greetings": (
        "Hey, {name}! Just send me few lines to start your need-to-do list. "
        "I can help you to arrange this list, go through it and strike "
        "out all the positions!"
    ),
    "good_luck": "Good luck!",
    "nice_work": "Nice work!",
    "help_1": (
        "Some useful actions: \n"
        "/del_list - Delete all your current todo items.\n"
        "/clean_list- Remove only checked items."
    ),
    "help_2": ("To check off the item simply send me its index number."),
    "to_start_help": (
        "To start a new to-do list, please, send me few text lines, e.g.: "
        '"Buy 10 oranges"'
    ),
    "no_items_to_check_off": (
        "It seems that you have no items in your to-do list to check off."
    ),
    "congrats": ("Congratulations! You have been finished you to-do list!"),
    "no_index": ("Sorry I cannot find to-do item with this index."),
}
