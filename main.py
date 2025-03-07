import os
from typing import Optional

import gradio as gr
from dotenv import load_dotenv
from langchain.chains import RetrievalQA
from langchain.llms.base import LLM
from langchain.schema import Document
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from mistralai import Mistral

# Load environment variables from .env if available.
load_dotenv()

# Environment variables for API keys and URLs.
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY", "default_key")
MISTRAL_API_URL = os.getenv("MISTRAL_API_URL", "https://api.mistral.ai")


class MistralLLM(LLM):
    """
    Custom LLM wrapper for the Mistral API.
    """

    def __init__(self, api_key, api_url) -> None:
        self.api_key = api_key
        self.api_url = api_url
        self.client = Mistral(api_key=api_key, api_url=api_url)

    @property
    def _llm_type(self) -> str:
        return "mistral"

    def _call(self, prompt: str, stop: Optional[list] = None) -> str:
        """
        Generates a response from the Mistral API based on the prompt.
        """
        response = self.client.generate(prompt, max_length=150)
        return response


def create_document_store() -> FAISS:
    """
    Creates a FAISS vector store from a set of Project Gutenberg documents.
    """
    documents = [
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
        # Add more documents as needed.
    ]

    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_documents(documents, embeddings)
    return vectorstore


def create_qa_chain(vectorstore: FAISS) -> RetrievalQA:
    """
    Sets up the RetrievalQA chain using the custom Mistral LLM and the FAISS vector store.
    """
    mistral_llm = MistralLLM(api_key=MISTRAL_API_KEY, api_url=MISTRAL_API_URL)
    qa_chain = RetrievalQA.from_chain_type(
        llm=mistral_llm, chain_type="stuff", retriever=vectorstore.as_retriever()
    )
    return qa_chain


def answer_query(query: str) -> str:
    """
    Retrieves relevant documents and generates an answer to the given query.
    """
    vectorstore = create_document_store()
    qa_chain = create_qa_chain(vectorstore)
    result = qa_chain.run(query)
    return result


def main() -> None:
    """
    Launches the Gradio interface for the RAG system.
    """
    iface = gr.Interface(
        fn=answer_query,
        inputs="text",
        outputs="text",
        title="Project Gutenberg RAG with Mistral API",
        description=(
            "Enter a question and get answers generated via Retrieval-Augmented Generation "
            "using Project Gutenberg documents."
        ),
    )
    iface.launch()


if __name__ == "__main__":
    main()
