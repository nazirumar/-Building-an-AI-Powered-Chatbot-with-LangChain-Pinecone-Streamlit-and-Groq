from src.helper import load_pdf_file, text_split, download_hugging_face_embeddings
from pinecone import Pinecone, ServerlessSpec
from langchain_pinecone import PineconeVectorStore
from dotenv import load_dotenv
import os

load_dotenv()

PINECONE_API_KEY=os.environ.get(key='PINECONE_API_KEY')
GROQ_API_KEY=os.environ.get(key='GROQ_API_KEY')

os.environ['PINECONE_API_KEY'] = PINECONE_API_KEY
os.environ['GROQ_API_KEY'] = GROQ_API_KEY

# Load PDF file
extracted_text = load_pdf_file(data="Data/")

# Split text into smaller chunks
text_chunks =  text_split(extracted_text)

# Download Hugging Face embeddings
embeddings = download_hugging_face_embeddings()


pc = Pinecone(api_key=PINECONE_API_KEY)

index_name = 'medicalbot'

pc.create_index(
  name=index_name,
  dimension=384,
  metric="cosine",
  spec=ServerlessSpec(
    cloud="aws",
    region="us-east-1"
  )
)



vector_store = PineconeVectorStore.from_documents(
    documents=text_chunks,
    index_name=index_name,
    embedding=embeddings,
)