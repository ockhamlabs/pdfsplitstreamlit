import streamlit as st
import PyPDF2
import os
from tempfile import mkdtemp
import shutil

def split_pdf_into_pages(pdf_file, output_folder):
    reader = PyPDF2.PdfFileReader(pdf_file)
    for page_num in range(reader.numPages):
        writer = PyPDF2.PdfFileWriter()
        writer.addPage(reader.getPage(page_num))
        output_filename = f"{output_folder}/{page_num+1:03d}.pdf"
        with open(output_filename, 'wb') as output_file:
            writer.write(output_file)

def create_zip(folder_path, zip_name):
    shutil.make_archive(zip_name, 'zip', folder_path)
    shutil.rmtree(folder_path)  # Clean up folder

st.title('PDF Splitter App')

uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
if uploaded_file is not None:
    with st.spinner('Splitting PDF...'):
        temp_dir = mkdtemp()
        split_pdf_into_pages(uploaded_file, temp_dir)
        zip_name = "split_pages"
        create_zip(temp_dir, zip_name)
        with open(f"{zip_name}.zip", "rb") as f:
            btn = st.download_button(
                label="Download ZIP",
                data=f,
                file_name=f"{zip_name}.zip",
                mime="application/zip"
            )
