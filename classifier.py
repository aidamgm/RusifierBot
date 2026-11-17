import re

from classification_rules import CATEGORY_RULES, CATEGORY_ORDER


class ProductClassifier:

    def classify(self, product):

        text = product["name"].lower()

        for category in CATEGORY_ORDER:

            if category == "Неопределенные":
                continue

            patterns = CATEGORY_RULES.get(category, [])

            for pattern in patterns:

                if re.search(pattern, text):

                    return category

        return "Неопределенные"


def sort_products(products):

    classifier = ProductClassifier()

    categories = {
        category: []
        for category in CATEGORY_ORDER
    }

    for product in products:

        category = classifier.classify(product)

        categories[category].append(product)

    # Убираем пустые категории
    return {
        category: items
        for category, items in categories.items()
        if items
    }