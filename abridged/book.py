# abridged/book.py

import PyPDF2

import re

def get_toc(
    pdf: PyPDF2.PdfReader,
    pages_toc: list[int],
    pattern: str,
    search_until_page: int
) -> dict[int, dict]:
    """Get the table of contents of a PDF file."""
    toc = dict()
    for i, (page_chapter, page_next_chapter) in enumerate(zip(pages_toc, pages_toc[1:])):
        text_page = pdf.pages[page_chapter].extract_text()
        match = re.search(pattern, text_page)
        if match:
            num, title = match.groups()
            if i == len(pages_toc)-1:
                page_next_chapter = search_until_page
            toc[int(num)] = {
                'title': title.strip().replace('\n', ' '),
                'since': page_chapter,
                'until': page_next_chapter-1
            }
        else:
            raise ValueError(f'No match in page {page_chapter}')
    return toc