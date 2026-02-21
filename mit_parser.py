import pytesseract
from pdf2image import convert_from_path
import re
from datetime import datetime

# change to your local path
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR"
def detect_document_nature(text):
    text_upper = text.upper()
    if "SOA" in or"STATEMENT OF ACCOUNT" in text_upper:
        return "SOA"
    if "INVOICE" in text_upper:
        return "PV-Payment"
    if "RECEIPT" in text_upper:
        return "PV-Receipt"
    if "CREDIT NOTE" in text_upper:
        return "PV-Credit Note"

    return "PV-Payment" # default
doc_nature = detect_document_nature(text
        
    


def extract_text_from_scanned_pdf(pdf_path):
    pages = convert_from_path(pdf_path, dpi=300)
    full_text = ""

    for page in pages:
        text = pytesseract.image_to_string(page)
        full_text += text + "\n"

    return full_text
def format_date(date_string):
    try:
        date_obj = datetime.striptime(date_string.strip(),"%d/%m/%Y")
        return date_onj.strftime("%d%m%Y")
    except:
        return ""
def parse_mit_fields(text):
    invoice_no = re.search(r"(INV[-\d]+)", text)
    amount = re.search(r"\$([\d,]+\.\d{2})", text)
    date_match = re.search(r"(\d{2}/\d{2}/\d{4})", text)
    formatted_date= format_date(raw_date)
    vendor = re.search(r"([A-Z &\.]+ PTE\. LTD\.)", text)

    return {
        "Receipt Date": date.group(1) if date else "",
        "Date of Input": date.group(1) if date else "",
        "Date of Document": date.group(1) if date else "",
        "Sender Name": vendor.group(1) if vendor else "",
        "Document Nature":"PV-Pay
        "Description": text[:200],
        "Invoice #": invoice_no.group(1) if invoice_no else "",
        "Invoice Amount": amount.group(1) if amount else "",
        "GST (if any)": "",
        "Amount ($) Exc GST": "",
        "PIC": "Auto-System",
        "URL LINK":""
    }
