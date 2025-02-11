import streamlit as st
from langchain_groq import ChatGroq
from langchain_pinecone import PineconeVectorStore
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from src.prompt import system_prompt
from src.helper import download_hugging_face_embeddings
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# API Keys
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")

if not GROQ_API_KEY or not PINECONE_API_KEY:
    st.error("⚠️ Missing API keys. Please check your .env file.")
    st.stop()

# Initialize Pinecone & Embeddings
embeddings = download_hugging_face_embeddings()
index_name = 'medicalbot'

docsearch = PineconeVectorStore.from_existing_index(
    index_name,
    embedding=embeddings
)
retriever = docsearch.as_retriever(
    search_type='similarity',
    search_kwargs={"k": 5}
)

# Initialize LLM
llm = ChatGroq(
    groq_api_key=GROQ_API_KEY,
    temperature=0.4,
    max_tokens=500
)

# Prompt Template
prompt_template = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("human", "{input}")
])

# Create Chains
question_answer_chain = create_stuff_documents_chain(llm, prompt_template)
rag_chain = create_retrieval_chain(retriever, question_answer_chain)

# Streamlit UI
st.set_page_config(page_title="Medical Chatbot", page_icon="💬", layout="wide")

st.title("💬 Medical Chatbot")
st.write("Ask me anything about medical topics.")

# Chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input
user_input = st.chat_input("Type your message here...")

if user_input:
    # Display user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Generate response
    try:
        response = rag_chain.invoke({"input": user_input})
        bot_reply = response['answer']
    except Exception as e:
        bot_reply = "⚠️ Error processing request. Please try again."

    # Display bot response
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
    with st.chat_message("assistant"):
        st.markdown(bot_reply)
