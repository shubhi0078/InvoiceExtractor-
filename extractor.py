import pdfplumber
import re
from llm import extract_with_llm


def extract_invoice_data(uploaded_file):

    text = ""

    # Read PDF
    with pdfplumber.open(uploaded_file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

    # Clean OCR/PDF spacing (e.g., "I N V O I C E" -> "INVOICE")
    clean_text = re.sub(
        r'\b(?:[A-Za-z]\s+){2,}[A-Za-z]\b',
        lambda m: m.group().replace(" ", ""),
        text
    )

    # Send the extracted text to the LLM
    data = extract_with_llm(clean_text)

    # Return data in the format expected by app.py
    return {
        "Invoice Number": data.get("Invoice Number", ""),
        "Invoice Date": data.get("Invoice Date", ""),
        "Vendor Name": data.get("Vendor Name", ""),
        "BL Number": data.get("BL Number", ""),
        "PO Number": data.get("PO Number", ""),
        "Amount": data.get("Amount", ""),
        "Currency": data.get("Currency", "")
    }