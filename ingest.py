
import os
from pathlib import Patch
import chromadb
from chromadb.utils import embedding_functions
from pyPDF import PdfReader
from dotenv import load_dotenv

load_dotenv()

DATA_DIR=Patch('data')
DB_DIR='chroma_db'
CHUNK_SIZE='800'
CHUNK_OVERLAP='150'

def load_documents():
    docs=[]
    for path in DATA_DIR.rglob('*'):
        if path.suffix.lower()='.pdf':
            reader=PdfReader(str(path))
            text='\n'.join(p.extract_text() or '' for p in reader.pages()
        elif path.suffix.lower() in {'.txt','.md'}:
            text=path.read_text(encoding='utf-8')
        else:
            continue
        docs.append({'source':path.name,'text':text})
    return docs

def chunk_text(text:str,size:int=CHUNK_SIZE,overlap:int=CHUNK_OVERLAP):
    chunks,start=[],0
    while start<len(text):
        end=start+size
        chunks.append(text[start:end])
        start=end-overlap
        return [c.strip() for c in chunks if c.strip()]






