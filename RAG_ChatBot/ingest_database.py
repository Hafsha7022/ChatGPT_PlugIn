from pathlib import Path
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_chroma import Chroma
from uuid import uuid4

# import the .env file
from dotenv import load_dotenv
SCRIPT_DIR = Path(__file__).resolve().parent
load_dotenv(SCRIPT_DIR / ".env")

# configuration
DATA_PATH = SCRIPT_DIR / "Data"
CHROMA_PATH = SCRIPT_DIR.parent / "chroma_db"

# initiate the embeddings model
embeddings_model = OpenAIEmbeddings(model="text-embedding-3-large")

# initiate the vector store
vector_store = Chroma(
    collection_name="example_collection",
    embedding_function=embeddings_model,
    persist_directory=str(CHROMA_PATH),
)

# loading the PDF document
loader = PyPDFDirectoryLoader(str(DATA_PATH))

raw_documents = loader.load()
if not raw_documents:
    raise ValueError(f"No PDF documents were loaded from '{DATA_PATH}'.")

# splitting the document
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=300,
    chunk_overlap=100,
    length_function=len,
    is_separator_regex=False,
)

# creating the chunks
chunks = text_splitter.split_documents(raw_documents)
if not chunks:
    raise ValueError(
        f"No text chunks were extracted from PDFs in '{DATA_PATH}'. "
        "Check that the PDFs contain extractable text."
    )

# creating unique ID's
uuids = [str(uuid4()) for _ in range(len(chunks))]

# adding chunks to vector store
vector_store.add_documents(documents=chunks, ids=uuids)