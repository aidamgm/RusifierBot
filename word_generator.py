from zipfile import ZipFile, ZIP_DEFLATED
from lxml import etree
import shutil
import os

from formatter import short_manufacturer

NS = {
    "w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
}


def generate_word(
    products,
    template="templates:template.docx",
    output="Rusifiers.docx"
):

    shutil.copyfile(template, output)

    with ZipFile(output, "r") as z:
        xml = z.read("word/document.xml")

    root = etree.fromstring(xml)

    texts = root.xpath("//w:t", namespaces=NS)

    placeholders = [
        t for t in texts
        if t.text in ("{{ title }}", "{{ manufacturer }}", "{{ expiry }}")
    ]

    for i, product in enumerate(products):

        # Если карточки закончились
        if i * 3 + 2 >= len(placeholders):
            break

        brand = str(product["brand"]).strip()
        title = str(product["name"]).strip()

        # Убираем повторения бренда в начале
        while title.upper().startswith(brand.upper()):
            title = title[len(brand):].strip()

        # Иногда после удаления остается MINA
        while title.upper().startswith("MINA "):
            title = title[5:].strip()

        title = f"{brand} {title}".strip()

        manufacturer = short_manufacturer(
            product["manufacturer"]
        )

        expiry = product["expiry"]

        placeholders[i * 3].text = title
        placeholders[i * 3 + 1].text = manufacturer
        placeholders[i * 3 + 2].text = expiry

    new_xml = etree.tostring(
        root,
        encoding="UTF-8",
        xml_declaration=True
    )

    tmp = "tmp.docx"

    with ZipFile(output, "r") as zin:
        with ZipFile(tmp, "w", ZIP_DEFLATED) as zout:

            for item in zin.infolist():

                if item.filename == "word/document.xml":
                    zout.writestr(item, new_xml)
                else:
                    zout.writestr(
                        item,
                        zin.read(item.filename)
                    )

    os.remove(output)
    os.rename(tmp, output)

    print(f"Заполнено карточек: {min(len(products), len(placeholders)//3)}")