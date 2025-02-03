# abridged/utils/pdf.py

from tqdm import tqdm
import tiktoken
import PyPDF2

from concurrent.futures import ProcessPoolExecutor

def extract_text_from_pages(pdf_path: str, start_page: int, end_page: int) -> str:
    """Extract text from a range of pages in a PDF file."""
    text = str()
    with open(pdf_path, 'rb') as file:
        pdf = PyPDF2.PdfReader(file)
        for i in range(start_page, end_page):
            text += pdf.pages[i].extract_text()
    return text

def describe_pdf(pdf_path: str, n_workers: int = 8) -> str:
    """Describe a PDF file (parallel version)."""
    with open(pdf_path, 'rb') as f:
        pdf = PyPDF2.PdfReader(f)
        n_pages = len(pdf.pages)
    pages_per_worker = max(1, n_pages // n_workers)
    page_ranges = [
        (i * pages_per_worker, min(n_pages, (i + 1) * pages_per_worker))
        for i in range(n_workers)
    ]
    with ProcessPoolExecutor(max_workers=n_workers) as executor:
        results = list(tqdm(
            executor.map(extract_text_from_pages, [pdf_path] * len(page_ranges), 
                         [r[0] for r in page_ranges], [r[1] for r in page_ranges]),
            total=len(page_ranges)
        ))
    full_text = ''.join(results)
    n_words = len(full_text.split())
    n_chars = len(full_text)
    encoding = tiktoken.encoding_for_model('gpt-4o')
    n_tokens = len(encoding.encode(full_text))
    return (
        f'This PDF file has {n_pages} pages.\n'
        f'It contains {n_words} words and {n_chars} characters.\n'
        f'It has {n_tokens} tokens according to the GPT-4o tokenizer.'
    )