import pdfplumber
import re

def extract_invoice_data(uploaded_file):

    text = ""

    # Read PDF
    with pdfplumber.open(uploaded_file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"

    # Clean text (removes spaces like I N V O I C E)
    clean_text = re.sub(
        r'\b(?:[A-Za-z]\s+){2,}[A-Za-z]\b',
        lambda m: m.group().replace(" ", ""),
        text
    )

    # Invoice Number
    invoice_number = re.search(
        r'INVOICE\s*NO\.?:\s*(\d+)',
        clean_text,
        re.IGNORECASE
    )

    # Invoice Date
    invoice_date = re.search(
        r'INVOICE\s*NO\.?:\s*\d+\s+(\d{2}\.\d{2}\.\d{4})',
        clean_text,
        re.IGNORECASE
    )

    # BL Number
    bl_number = re.search(
        r'B/L[- ]?NO\.?\s*([A-Z0-9]+)',
        clean_text,
        re.IGNORECASE
    )

    # Gross Amount and Currency
    gross = re.search(
        r'GROSS\s+([\d,.]+)\s+([A-Z]{3})',
        clean_text,
        re.IGNORECASE
    )

    return {
        "Invoice Number": invoice_number.group(1) if invoice_number else "",
        "Invoice Date": invoice_date.group(1) if invoice_date else "",
        "BL Number": bl_number.group(1) if bl_number else "",
        "Amount": gross.group(1) if gross else "",
        "Currency": gross.group(2) if gross else ""
    }