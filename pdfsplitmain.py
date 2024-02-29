import streamlit as st
import PyPDF2
import os
from tempfile import mkdtemp, NamedTemporaryFile
import shutil
import zipfile

def split_pdf_into_pages(pdf_file, output_folder):
    reader = PyPDF2.PdfReader(pdf_file)
    # Extracting the first 8 characters of the original filename without its extension
    original_filename_prefix = os.path.splitext(os.path.basename(pdf_file.name))[0][:8]
    for page_num in range(len(reader.pages)):
        writer = PyPDF2.PdfWriter()
        writer.add_page(reader.pages[page_num])
        # Including the original filename prefix in the output filename
        output_filename = f"{output_folder}/{original_filename_prefix}_Page_{page_num+1:03d}.pdf"
        with open(output_filename, 'wb') as output_file:
            writer.write(output_file)

def zip_files(directory):
    zip_filename = os.path.join(directory, "split_pages.zip")
    with zipfile.ZipFile(zip_filename,'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file != "split_pages.zip":  # Avoid including the zip file itself
                    zipf.write(os.path.join(root, file), file)
    return zip_filename

st.title('PDF Splitter App')

uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])
if uploaded_file is not None:
    temp_dir = mkdtemp()
    split_pdf_into_pages(uploaded_file, temp_dir)
    zip_path = zip_files(temp_dir)

    with open(zip_path, "rb") as f:
        st.download_button(
            label="Download Split Pages as ZIP",
            data=f,
            file_name="split_pages.zip",
            mime="application/zip"
        )

    # Cleanup
    shutil.rmtree(temp_dir)  # Remove temporary directory and files after downloading
