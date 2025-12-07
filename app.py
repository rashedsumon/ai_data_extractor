import streamlit as st
import os
from extractor import extract_excel, extract_pdf, populate_excel_template, populate_word_template
from data_loader import download_dataset

# Create folders
os.makedirs("uploads", exist_ok=True)
os.makedirs("logs", exist_ok=True)

st.title("AI-Powered Data Extractor")
st.write("Upload Excel/PDF files to extract data and populate templates.")

# Step 1: Download dataset (optional)
if st.button("Download Example Dataset"):
    dataset_path = download_dataset()
    st.success(f"Dataset downloaded at {dataset_path}")

# Step 2: File upload
uploaded_files = st.file_uploader("Upload Excel/PDF files", type=["xlsx", "pdf"], accept_multiple_files=True)

# Step 3: Template selection
template_type = st.selectbox("Select template type", ["Excel", "Word"])
template_file = st.file_uploader("Upload template file", type=["xlsx", "docx"])

# Step 4: Process files
if st.button("Process Files") and uploaded_files and template_file:
    for uploaded_file in uploaded_files:
        file_path = os.path.join("uploads", uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        if uploaded_file.name.endswith(".xlsx"):
            df = extract_excel(file_path)
            if template_type == "Excel":
                output_path = f"uploads/output_{uploaded_file.name}"
                populate_excel_template(df, template_file, output_path)
                st.success(f"Excel populated: {output_path}")
        elif uploaded_file.name.endswith(".pdf"):
            text = extract_pdf(file_path)
            if template_type == "Word":
                output_path = f"uploads/output_{uploaded_file.name.replace('.pdf','.docx')}"
                populate_word_template(text, template_file, output_path)
                st.success(f"Word populated: {output_path}")
