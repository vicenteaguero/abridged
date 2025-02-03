# abridged/pdf.py

from tqdm import tqdm
import PyPDF2

from concurrent.futures import ProcessPoolExecutor

def search_in_pdf(
    pdf_path: str,
    search: str,
    start_page: int,
    end_page: int
) -> list[int]:
    """Search for a string in a range of pages of a PDF file."""
    matches = []
    with open(pdf_path, 'rb') as f:
        pdf = PyPDF2.PdfReader(f)
        for i in range(start_page, end_page):
            text = pdf.pages[i].extract_text()
            if text and search in text:
                matches.append(i)
    return matches

def parallel_search_in_pdf(
    pdf_path: str,
    search: str,
    start_page: int,
    end_page: int,
    n_workers: int = 4,
) -> list[int]:
    """Parallel search for a string in a range of pages of a PDF file."""
    n_pages = end_page-start_page
    pages_per_worker = max(1, n_pages//n_workers)
    page_ranges = [
        (
            (start_page-1)+(i*pages_per_worker),
            min(end_page, start_page+(i+1)*pages_per_worker)
        )
        for i in range(n_workers)
    ]
    with ProcessPoolExecutor(max_workers=n_workers) as executor:
        results = list(tqdm(
            executor.map(
                search_in_pdf,
                [pdf_path]*n_workers,
                [search]*n_workers,
                [r[0] for r in page_ranges],
                [r[1] for r in page_ranges]
            ),
            total=n_workers
        ))
    return sorted(set().union(*results))