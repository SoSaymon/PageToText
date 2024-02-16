from typing import List

from bs4 import BeautifulSoup
import ebooklib
from ebooklib import epub


def epub2html(epub_path: str) -> List:
    book = epub.read_epub(epub_path)
    chapters = []
    for item in book.get_items():
        if item.get_type() == ebooklib.ITEM_DOCUMENT:
            chapters.append(item.get_content())

    return chapters


def chapter2text(chapter: str) -> str:
    output = ""
    soup = BeautifulSoup(chapter, "html.parser")
    text = soup.find_all(string=True)
    for t in text:
        if t.parent.name not in blacklist:
            output += "{} ".format(t)

    return output


def thtml2ttext(thtml):
    output = []
    for html in thtml:
        text = chapter2text(html)
        output.append(text)

    return output


def epub2text(epub_path):
    chapters = epub2html(epub_path)
    ttext = thtml2ttext(chapters)
    return ttext


def output_text(text):
    with open("output.txt", "w", encoding="utf-8") as f:
        for t in text:
            f.write(t)


if __name__ == "__main__":
    path = "ebook.epub"
    blacklist = [
        "[document]",
        "noscript",
        "header",
        "html",
        "meta",
        "head",
        "input",
        "script",
    ]

    out = epub2text(path)
    output_text(out)
