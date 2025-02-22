import os
import re
from settings import settings
from PyPDF2 import PdfReader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from db_operations import DatabaseManager

db_manager = DatabaseManager()


def cleaned_text(text):
    clean_text = re.sub(r"\n\s*\n", "\n", text)  # Remove blank lines (multiple newlines)
    clean_text = re.sub(r"[ \t]+", " ", clean_text)
    return clean_text


def process_text(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()
    return cleaned_text(text)


def process_pdf_text(file_path):
    documents = []
    reader = PdfReader(file_path)
    num_pages = len(reader.pages)
    for i in range(num_pages):
        page = reader.pages[i]
        text = cleaned_text(page.extract_text())
        doc = Document(page_content=text, metadata = {"file_path":file_path})
        documents.append(doc)
    return documents


def get_files_list(folder_path):
    files = os.listdir(folder_path)
    return files


def get_processed_files():
    processed_path = settings.PROCESSED_FILES
    if not os.path.exists(processed_path):
        with open(processed_path, 'w') as f:
            return set()
    else:
        with open(processed_path, 'r') as f:
            data = f.readlines()
            return {data.replace('\n','') for data in data}


def get_chunks(documents):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=settings.CHUNK_SIZE, chunk_overlap=settings.CHUNK_OVERLAP)
    chunks = text_splitter.split_documents(documents)
    return chunks


def process_files():
    processed_files = get_processed_files()
    files = get_files_list(settings.TEXT_FOLDER_PATH)
    new_processed_files = set(files) - processed_files
    if new_processed_files:
        with open(settings.PROCESSED_FILES, 'a+', encoding="utf-8") as f:
            documents = []
            for file in new_processed_files:
                file_path = os.path.join(settings.TEXT_FOLDER_PATH,file)
                if file.endswith('.pdf'):
                    pdf_document = process_pdf_text(file_path)
                    documents.extend(pdf_document)
                elif file.endswith('.txt'):
                    text = process_text(file_path)
                    doc = Document(page_content=text, metadata = {"file_path":file_path})
                    documents.append(doc)
                f.write(file + '\n') 
            chunks = get_chunks(documents)
            return chunks
    return []