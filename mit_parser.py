import pytesseract
from pdf2image import convert_from_path, conver_from_bytes
import re
from datetime import datetime
import sys
import pytesseract

# ✅ MUST point to the exe, not folder
if sys.platform.startswith("win"):
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def detect_document_type(pdf_path:str) -> str:
    """
    Returns (Document Nature, Document Category)
    Based on keyword detection from OCR text.
    """
    text_upper = (text or "").upper()

    # SOA / Statement of Account
    if "STATEMENT OF ACCOUNT" in text_upper or re.search(r"\bSOA\b", text_upper):
        return "PV-Payment", "SOA"

    # Credit Note
    if "CREDIT NOTE" in text_upper:
        return "PV-Payment", "CREDIT NOTE"

    # Receipt
    if "RECEIPT" in text_upper:
        return "PV-Receipt", "RECEIPT"

    # Invoice
    if "INVOICE" in text_upper:
        return "PV-Payment", "SUPPLIER INVOICE"

    # Default
    return "PV-Payment", "SUPPLIER INVOICE"


def extract_text_from_scanned_pdf(pdf_path: str) -> str:
    pages = convert_from_path(pdf_path, dpi=300)
    full_text = ""

    for page in pages:
        page_text = pytesseract.image_to_string(page)
        full_text += page_text + "\n"

    return full_text


def format_date(date_string: str) -> str:
    """
    Normalize date string to DD/MM/YYYY.
    Supports: 14/04/2025 and 15/4/2025.
    """
    if not date_string:
        return ""

    s = date_string.strip()

    for fmt in ("%d/%m/%Y", "%d/%m/%y"):
        try:
            date_obj = datetime.strptime(s, fmt)
            return date_obj.strftime("%d/%m/%Y")
        except ValueError:
            continue

    # handle cases like 15/4/2025 (single digit month/day)
    m = re.search(r"(\d{1,2})/(\d{1,2})/(\d{4})", s)
    if m:
        try:
            d, mo, y = m.group(1), m.group(2), m.group(3)
            date_obj = datetime.strptime(f"{int(d):02d}/{int(mo):02d}/{y}", "%d/%m/%Y")
            return date_obj.strftime("%d/%m/%Y")
        except ValueError:
            pass

    return ""


def parse_mit_fields(text: str) -> dict:
    # Document type
    doc_nature, doc_category = detect_document_type(text)

    # Extract common fields (best-effort; OCR varies)
    invoice_no_match = re.search(r"\bINV[-\s]?\d{4}[-\s]?\d+\b|\bINV[-\d]+\b", text, re.IGNORECASE)
    amount_match = re.search(r"\$?\s*([\d,]+\.\d{2})", text)
    date_match = re.search(r"(\d{1,2}/\d{1,2}/\d{4})", text)

    vendor_match = re.search(r"([A-Z0-9 &\.\-]+(?:PTE\.?\s*LTD\.?|LTD\.?))", text.upper())

    raw_date = date_match.group(1) if date_match else ""
    formatted_date = format_date(raw_date)

    invoice_no = invoice_no_match.group(0).replace(" ", "") if invoice_no_match else ""
    amount = amount_match.group(1) if amount_match else ""
    vendor = vendor_match.group(1).strip() if vendor_match else ""

    # Description: you can refine later (e.g., first 2 lines after INVOICE)
    description = " ".join(text.split())[:200]

    return {
        "Receipt Date Stamped": formatted_date,
        "Date of Input": formatted_date,
        "Date of Document": formatted_date,
        "Due Date (If Applicable)": "",
        "Sender Name": vendor,
        "Document Nature": doc_nature,
        "Document Category": doc_category,
        "Description": description,
        "Invoice #": invoice_no,
        "Tracking Number": "",
        "Invoice amount": amount,
        "GST (if any)": "",
        "Amount ($) Exc GST": "",
        "PIC": "Auto-System",
        "URL LINK": ""
    }
