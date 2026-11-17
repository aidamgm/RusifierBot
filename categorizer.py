import re

# Ключевые слова -> категория
CATEGORY_RULES = {

    "Губы": [
        "помада",
        "блеск",
        "тинт",
        "масло для губ",
        "карандаш для губ",
        "lip",
    ],

    "Глаза": [
        "тушь",
        "тени",
        "подводка",
        "лайнер",
        "карандаш для глаз",
        "база для век",
        "eyeliner",
        "mascara",
    ],

    "Лицо": [
        "тональный",
        "пудра",
        "румяна",
        "хайлайтер",
        "бронзер",
        "консилер",
        "корректор",
        "праймер",
        "кушон",
        "скульптор",
    ],

    "Ногти": [
        "лак",
        "гель-лак",
        "base coat",
        "top coat",
    ],

    "Кисти": [
        "кисть",
        "спонж",
        "аппликатор",
    ],

}


def detect_category(name: str):

    text = name.lower()

    for category, words in CATEGORY_RULES.items():

        for word in words:

            if word in text:
                return category

    return "Неопределенные"


def sort_products(products):

    result = {}

    for product in products:

        category = detect_category(product["name"])

        result.setdefault(category, []).append(product)

    return result