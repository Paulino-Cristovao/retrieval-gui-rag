import os
from typing import List

import gradio as gr
from dotenv import load_dotenv

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
from langchain_mistralai.chat_models import ChatMistralAI
from langchain_mistralai.embeddings import MistralAIEmbeddings
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain

# -----------------------------------------------------------------------------
# Load environment variables from a .env file (if available)
load_dotenv()
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY", "")
if not MISTRAL_API_KEY:
    raise EnvironmentError("Please set MISTRAL_API_KEY in your environment or .env file.")

# -----------------------------------------------------------------------------
# Create a simple document store
def create_document_store():
    docs = [
        Document(
            page_content=(
                "It is a truth universally acknowledged, that a single man in possession "
                "of a good fortune, must be in want of a wife..."
            ),
            metadata={
                "title": "Pride and Prejudice",
                "url": "https://www.gutenberg.org/ebooks/1342",
            },
        ),
        Document(
            page_content=(
                "You will rejoice to hear that no disaster has accompanied the commencement "
                "of an enterprise, which you have regarded with such evil forebodings..."
            ),
            metadata={
                "title": "Frankenstein",
                "url": "https://www.gutenberg.org/ebooks/84",
            },
        ),
        Document(
            page_content=(
                "This is Maiva community located in northern Mozambique. The community is "
                "known for its rich culture and traditions..."
                "There is a famous family called the Muhimuas, the leader was a young Paulino..."
            ),
            metadata={
                "title": "Maiva Community",
                "url": "https://www.maivacommunity.com/",
            },
        ),
    ]
    
    # Initialize embeddings using official MistralAI integration
    embeddings = MistralAIEmbeddings(model="mistral-embed", mistral_api_key=MISTRAL_API_KEY)
    
    # Create vector store
    vector_store = FAISS.from_documents(docs, embeddings)
    return vector_store

# -----------------------------------------------------------------------------
# Define the prompt template
prompt = ChatPromptTemplate.from_template("""Answer the following question based only on the provided context:

<context>
{context}
</context>

Question: {input}""")

# -----------------------------------------------------------------------------
# Define the query-answering function
def answer_query(query: str) -> str:
    if not query.strip():
        return "Please enter a valid query."
    
    # Create vector store and retriever
    vector_store = create_document_store()
    retriever = vector_store.as_retriever(search_kwargs={"k": 4})
    
    # Initialize the LLM
    model = ChatMistralAI(
        model="mistral-large-latest",
        temperature=0.7,
        mistral_api_key=MISTRAL_API_KEY
    )
    
    # Create retrieval chain
    document_chain = create_stuff_documents_chain(model, prompt)
    retrieval_chain = create_retrieval_chain(retriever, document_chain)
    
    # Run the query
    response = retrieval_chain.invoke({"input": query})
    return response["answer"].strip()

# -----------------------------------------------------------------------------
# Launch the Gradio interface
def main() -> None:
    interface = gr.Interface(
        fn=answer_query,
        inputs=gr.Textbox(lines=2, placeholder="Enter your question here..."),
        outputs="text",
        title="Project Gutenberg RAG with Mistral API",
        description=(
            "Enter a question and get an answer generated via Retrieval-Augmented Generation "
            "using Project Gutenberg documents and Mistral AI."
        )
    )
    interface.launch(share=True)

if __name__ == "__main__":
    main()
