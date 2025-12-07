import os
import pandas as pd
import pdfplumber
from docx import Document
import pytesseract
from PIL import Image

# Utility functions
def extract_excel(file_path):
    try:
        df = pd.read_excel(file_path, engine="openpyxl")
        return df
    except Exception as e:
        print(f"Error reading Excel {file_path}: {e}")
        return None

def extract_pdf(file_path):
    text_data = ""
    try:
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                text_data += page.extract_text() or ""
    except:
        # fallback OCR for scanned PDFs
        from pdf2image import convert_from_path
        pages = convert_from_path(file_path)
        for page in pages:
            text_data += pytesseract.image_to_string(page)
    return text_data

def populate_excel_template(df, template_path, output_path):
    try:
        template_df = pd.read_excel(template_path, engine="openpyxl")
        # Example: append extracted data
        result_df = pd.concat([template_df, df], ignore_index=True)
        result_df.to_excel(output_path, index=False)
    except Exception as e:
        print(f"Error populating Excel template: {e}")

def populate_word_template(text, template_path, output_path):
    try:
        doc = Document(template_path)
        for p in doc.paragraphs:
            if "{{data}}" in p.text:
                p.text = p.text.replace("{{data}}", text)
        doc.save(output_path)
    except Exception as e:
        print(f"Error populating Word template: {e}")
