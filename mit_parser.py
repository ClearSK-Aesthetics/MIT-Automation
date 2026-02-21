import pytesseract
from pdf2image import convert_from_path
import re

# change to your local path
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR"


def extract_text_from_scanned_pdf(pdf_path):
    pages = convert_from_path(pdf_path, dpi=300)
    full_text = ""

    for page in pages:
        text = pytesseract.image_to_string(page)
        full_text += text + "\n"

    return full_text


def parse_mit_fields(text):
    """
    acocoridng to key words to extract MIT Columns
    Based on MIT format to expand
    """

    vendor = re.search(r"(Supplier|Vendor)\s*:?\s*(.+)", text)
    amount = re.search(r"(Total|Amount)\s*:?\s*\$?([\d,]+\.\d{2})", text)
    date = re.search(r"(Date)\s*:?\s*(\d{2}/\d{2}/\d{4})", text)

    return {
        "Vendor": vendor.group(2) if vendor else "Unknown",
        "Amount": amount.group(2) if amount else "0",
        "Date": date.group(2) if date else "Unknown",
        "Raw_Text": text[:500]
    }
