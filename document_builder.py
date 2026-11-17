from zipfile import ZipFile, ZIP_DEFLATED
from lxml import etree
import shutil
import os

NS = {
    "w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
}


def build_document(
    products,
    template="templates/template.docx",
    output="Rusifiers.docx"
):
    shutil.copyfile(template, output)

    with ZipFile(output, "r") as z:
        xml = z.read("word/document.xml")

    root = etree.fromstring(xml)

    # Убираем разреженный интервал у {{ title }}
    for r in root.xpath("//w:r", namespaces=NS):
        texts = r.xpath("./w:t", namespaces=NS)

        if not texts:
            continue

        text = texts[0].text

        if text and "{{ title }}" in text:
            rpr = r.find("w:rPr", NS)

            if rpr is not None:
                spacing = rpr.find("w:spacing", NS)

                if spacing is not None:
                    rpr.remove(spacing)

    texts = root.xpath("//w:t", namespaces=NS)

    titles = []
    manufacturers = []

    for t in texts:
        if not t.text:
            continue

        if "{{ title }}" in t.text:
            titles.append(t)
        elif "{{ manufacturer }}" in t.text:
            manufacturers.append(t)

    print(f"Title placeholders: {len(titles)}")
    print(f"Manufacturer placeholders: {len(manufacturers)}")

    for i, product in enumerate(products):
        if i >= len(titles) or i >= len(manufacturers):
            break

        title = product["name"].strip()
        brand = product["brand"].strip()

        while brand and title.upper().startswith(brand.upper()):
            title = title[len(brand):].strip()

        title = f"{brand} {title}."

        titles[i].text = f"{title}. "
        manufacturers[i].text = product["manufacturer"]

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

    print("Готово!")