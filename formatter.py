import re


def short_manufacturer(text):

    match = re.search(r'"([^"]+)"', text)

    if match:
        return match.group(1)

    return text 