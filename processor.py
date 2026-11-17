from excel import read_excel
from classifier import sort_products
from document_builder_v2 import build_document_v2

def process_excel(input_file):

    products = read_excel(input_file)

    if not products:
        return [], {}

    categories = sort_products(products)

    print("\n=== Результат классификации ===")

    for category, items in categories.items():
        print(f"{category}: {len(items)} товаров")

    filename = "Rusifiers.docx"

    build_document_v2(
        categories,
        template="templates/template_v2.docx",
        output=filename
    )

    return [filename], categories
