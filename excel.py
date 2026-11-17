from openpyxl import load_workbook


def read_excel(filename):

    wb = load_workbook(filename)
    ws = wb.active

    products = []

    for row in ws.iter_rows(min_row=2, values_only=True):

        if not row[0]:
            continue

        product = {
            "sku": str(row[0]).replace(".0", ""),
            "name": row[1] or "",
            "brand": row[2] or "",
            "manufacturer": row[3] or "",
            "expiry": "см. на упаковке",
        }

        products.append(product)

    return products

