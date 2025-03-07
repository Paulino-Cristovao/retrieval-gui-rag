# retrieval-gui-rag
# Retrieval-Augmented Generation (RAG) with Mistral API and LangChain

This project demonstrates a retrieval-augmented generation (RAG) system built using LangChain and Gradio. It uses documents from Project Gutenberg as the data source and integrates a custom Mistral API LLM for generating answers. The system retrieves relevant documents using a FAISS vector store and displays answers via a simple Gradio web interface.

## Features

- **Custom Mistral API LLM:** Integrates the Mistral API as a LangChain LLM.
- **Document Retrieval:** Uses a FAISS index for efficient similarity search over Project Gutenberg documents.
- **Gradio GUI:** Provides a web interface for users to input queries and view generated responses.
- **CI/CD:** Includes GitHub Actions for automated testing, linting, and type checking.
- **Pre-commit Hooks:** Uses pre-commit to enforce code style with Ruff, type checking with MyPy, and formatting with Black and isort.

## Getting Started

### Prerequisites

- Python 3.7 or later

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/retrieval-gui-rag.git
   cd retrieval-gui-rag
