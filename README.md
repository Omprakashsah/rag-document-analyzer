# RAG Doc Analyzer

**Analyze, summarize, generate insights, and create MCQs from your documents using the power of OpenAI models and Streamlit.**  

This application leverages **Retrieval-Augmented Generation (RAG)** to provide context-aware responses and actionable insights from your text data.

---

## ✨ Features

This tool is a complete solution for interacting with your documents:

- **Multi-Format Support:** Easily upload PDF or CSV documents.  
- **Intelligent Analysis:** Generate concise summaries and key insights.  
- **MCQ Generation:** Create multiple-choice questions to test comprehension.  
- **Interactive Chat:** Chat directly with your document using OpenAI GPT models.  
- **Powerful RAG Engine:** Build a retrieval index (FAISS) for highly accurate, contextual answers.  
- **Clean UI:** Beautiful and responsive interface built with Streamlit.  
- **Secure API Handling:** Safely manage your API keys using a `.env` file.

---

## 💻 Tech Stack

| Layer       | Tools & Frameworks      | Description                                           |
|------------|------------------------|-------------------------------------------------------|
| Frontend   | Streamlit              | Web framework for building the user interface.      |
| Backend    | Python 3.9+            | Core language for all logic.                        |
| AI Models  | OpenAI (GPT-4o, GPT-3.5)| Large language models used for analysis and generation. |
| RAG        | LangChain, FAISS       | Libraries for building the RAG pipeline and vector indexing. |
| PDF Processing | PyPDF2              | Utility for extracting text from PDF files.         |
| Environment | python-dotenv          | Securely loads environment variables from `.env`.   |

---

## 🚀 Getting Started

### Clone the Repository
```bash
git clone https://github.com/your-username/rag-doc-analyzer.git
cd rag-doc-analyzer

## Set Up Your Environment

It's highly recommended to use a **virtual environment**.

### Create a Virtual Environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

Install all required libraries in one go:

pip install -r requirements.txt

Add Your OpenAI API Key

Create a .env file in the root directory of the project:

touch .env

Open the .env file and add your secret key:

OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

Run the App

Launch the Streamlit application:

streamlit run streamlit_app.py
Your browser should automatically open the app at http://localhost:8501
