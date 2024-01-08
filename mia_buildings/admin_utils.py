from bs4 import BeautifulSoup


def validate_and_clean_content_markup(html: str) -> (bool, str):
    soup = BeautifulSoup(html, "html.parser")
    before = soup.prettify()
    cleanup(soup)
    after = soup.prettify()
    return before == after, after


def cleanup(document: BeautifulSoup) -> None:
    ATTRIBUTE_WHITELIST = ["href", "src"]
    ELEMENT_WHITELIST = ["p", "a", "em", "strong"]

    def removeAttributes(element):
        for attr in set(element.attrs):
            if attr not in ATTRIBUTE_WHITELIST:
                del element[attr]

    def removeEmptyElement(element):
        if len(element.get_text(strip=True)) == 0:
            element.extract()

    def unwrapElement(element):
        if element.name not in ELEMENT_WHITELIST:
            element.unwrap()

    def cleanupElement(element):
        removeAttributes(element)
        unwrapElement(element)
        removeEmptyElement(element)

    result = document.find_all()
    for entry in result:
        cleanupElement(entry)
