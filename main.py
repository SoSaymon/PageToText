from typing import List

import ebooklib
from bs4 import BeautifulSoup
from ebooklib import epub
from spire.pdf import PdfDocument


def epub2html(epub_path: str) -> List[str]:
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


def thtml2ttext(thtml: List[str]) -> List[str]:
    output = []
    for html in thtml:
        text = chapter2text(html)
        output.append(text)

    return output


def epub2text(epub_path: str) -> List[str]:
    chapters = epub2html(epub_path)
    ttext = thtml2ttext(chapters)
    return ttext


def output_text(text: List[str]) -> None:
    with open("output.txt", "w", encoding="utf-8") as f:
        for t in text:
            f.write(t)


def pdf2list(pdf_path: str) -> List[str]:
    doc = PdfDocument()
    doc.LoadFromFile(pdf_path)

    list_ = []

    for i in range(doc.Pages.Count):
        page = doc.Pages.get_Item(i)
        text = page.ExtractText(True)
        list_.append(text)

    doc.Close()

    return list_


def list2text(list_: List[str]) -> None:
    with open("output.txt", "w", encoding="utf-8") as f:
        for text in list_:
            f.write(text + "\n")


if __name__ == "__main__":
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

    choice = input("Do you want to convert PDF or EPUB? (pdf/epub): ")

    if choice == "pdf":
        path = "ebook.pdf"
        out = pdf2list(path)
        list2text(out)
    elif choice == "epub":
        path = "ebook.epub"
        out = epub2text(path)
        output_text(out)
    else:
        print("Invalid choice")
