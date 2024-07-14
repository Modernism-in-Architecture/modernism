from bs4 import BeautifulSoup

ATTRIBUTE_WHITELIST = ["href", "src"]
ELEMENT_WHITELIST = ["p", "a", "em", "strong"]


def validate_and_clean_content_markup(html: str) -> tuple[bool, str]:
    soup = BeautifulSoup(html, "html.parser")
    before = str(soup)
    cleanup(soup)
    after = str(soup)
    return before == after, after


def cleanup(document: BeautifulSoup) -> None:
    def remove_attributes(element):
        for attr in set(element.attrs):
            if attr not in ATTRIBUTE_WHITELIST:
                del element[attr]

    def remove_empty_element(element):
        if len(element.get_text(strip=True)) == 0:
            element.extract()

    def unwrap_element(element):
        if element.name not in ELEMENT_WHITELIST:
            element.unwrap()

    def cleanup_element(element):
        remove_attributes(element)
        unwrap_element(element)
        remove_empty_element(element)

    result = document.find_all()
    for entry in result:
        cleanup_element(entry)
