from math import ceil


CARDS_PER_TABLE = 20


def calculate_tables(products_count):

    return ceil(products_count / CARDS_PER_TABLE)


def calculate_pages(products_count):

    tables = calculate_tables(products_count)

    return ceil(tables / 2)


if __name__ == "__main__":

    products = 111

    tables = calculate_tables(products)
    pages = calculate_pages(products)

    print(f"Товаров: {products}")
    print(f"Таблиц: {tables}")
    print(f"Страниц: {pages}")