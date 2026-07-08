import streamlit as st
import pandas as pd
from extractor import extract_invoice_data
from io import BytesIO

st.set_page_config(page_title="Invoice Extractor")

st.title("📄 Invoice Extraction Tool")

uploaded_files = st.file_uploader(
    "Upload PDF invoices",
    type=["pdf"],
    accept_multiple_files=True
)

if uploaded_files:

    results = []

    progress = st.progress(0)

    for i, file in enumerate(uploaded_files):

        try:
            data = extract_invoice_data(file)
            data["File Name"] = file.name
            data["Status"] = "Success"

        except Exception as e:
            data = {
                "File Name": file.name,
                "Invoice Number": "",
                "Invoice Date": "",
                "BL Number": "",
                "Amount": "",
                "Currency": "",
                "Status": f"Error: {str(e)}"
            }

        results.append(data)
        progress.progress((i + 1) / len(uploaded_files))

    # Everything below runs ONLY ONCE after all PDFs are processed

    df = pd.DataFrame(results)

    st.success(f"{len(df)} invoice(s) processed successfully!")

    st.dataframe(df, use_container_width=True)

    output = BytesIO()

    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Invoices")

    output.seek(0)

    st.download_button(
        label="📥 Download Excel",
        data=output,
        file_name="Invoice_Extraction.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        key="download_excel"
    )