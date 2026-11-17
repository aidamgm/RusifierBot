from copy import deepcopy
from docx import Document
from docx.oxml.ns import qn

CARDS_PER_ROW = 5


def remove_spacing(run):
    rpr = run._element.rPr
    if rpr is None:
        return
    spacing = rpr.find(qn("w:spacing"))
    if spacing is not None:
        rpr.remove(spacing)


def normalize_title(product):
    title = product["name"].strip()
    brand = product["brand"].strip()
    while brand and title.upper().startswith(brand.upper()):
        title = title[len(brand):].strip()
    return f"{brand} {title}."


def write_title(run, product):
    paragraph = run._parent

    title = product["name"].strip()
    brand = product["brand"].strip()

    while brand and title.upper().startswith(brand.upper()):
        title = title[len(brand):].strip()

    # очищаем существующий run
    run.text = ""

    # бренд
    brand_run = paragraph.add_run(brand)
    brand_run.bold = True

    # копируем форматирование
    if run._element.rPr is not None:
        brand_run._element.get_or_add_rPr().append(
            deepcopy(run._element.rPr)
        )
        brand_run.bold = True

    # остальной текст
    title_run = paragraph.add_run(f" {title}.\n")

    if run._element.rPr is not None:
        title_run._element.get_or_add_rPr().append(
            deepcopy(run._element.rPr)
        )

 
def get_placeholders(row):
    placeholders = []
    for cell in row.cells:
        for paragraph in cell.paragraphs:
            for run in paragraph.runs:
                text = run.text
                if "{{ category }}" in text:
                    placeholders.append(("category", run))
                elif "{{ title }}" in text:
                    placeholders.append(("title", run))
                elif "{{ manufacturer }}" in text:
                    placeholders.append(("manufacturer", run))
    return placeholders


def fill_row(row, products, category=""):
    placeholders = get_placeholders(row)
    product_index = 0
    category_written = False

    for kind, run in placeholders:
        if kind == "category":
            if not category_written:
                run.text = category
                category_written = True
            else:
                run.text = ""
            remove_spacing(run)
            continue

        if product_index >= len(products):
            run.text = ""
            remove_spacing(run)
            continue

        product = products[product_index]

        if kind == "title":
            run.text = normalize_title(product)
        elif kind == "manufacturer":
            run.text = product["manufacturer"]
            product_index += 1

        remove_spacing(run)


def build_document_v2(
    categories,
    template="templates/template_v2.docx",
    output="Rusifiers.docx"
):
    doc = Document(template)

    category_paragraph = None

    for paragraph in doc.paragraphs:
        if "{{ category }}" in paragraph.text:
            category_paragraph = paragraph
            break

    table = doc.tables[0]

    template_row = table.rows[0]
    template_tr = deepcopy(template_row._tr)

    # удаляем все строки, кроме шаблонной
    while len(table.rows) > 1:
        table._tbl.remove(table.rows[-1]._tr)

    current_row = 0

    for category_name, products in categories.items():
        if category_paragraph:
            category_paragraph.text = category_name
        start = 0
        first_row = True

        while start < len(products):
            # если строки закончились — копируем шаблонную
            if current_row >= len(table.rows):
                table._tbl.append(deepcopy(template_tr))

            row = table.rows[current_row]
            chunk = products[start:start + CARDS_PER_ROW]

            print(
                f"Категория: {category_name}, первая={first_row}, товаров={len(chunk)}",
                flush=True
            )

            fill_row(
                row,
                chunk,
                category_name if first_row else ""
            )

            first_row = False
            current_row += 1
            start += CARDS_PER_ROW

    doc.save(output)
    print("Готово!")