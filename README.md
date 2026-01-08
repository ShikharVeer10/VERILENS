# VERILENS

VERILENS is a document processing and retrieval system that implements a RAG (Retrieval-Augmented Generation) pipeline for intelligent document analysis and querying.

## 🎯 Overview

VERILENS provides a robust framework for:
- **Document Ingestion**: Loading and processing PDF and text documents
- **Smart Chunking**: Breaking down large documents into manageable, overlapping chunks for better context preservation
- **Vector Embeddings**: Converting text chunks into vector representations using TF-IDF
- **Intelligent Retrieval**: Finding relevant document chunks based on semantic similarity
- **Answer Generation**: Generating answers with citations using Groq's LLM API
- **Verification**: Optional answer verification to ensure responses are grounded in source documents

## 🏗️ Architecture

```
app/
├── core/
│   ├── agent/
│   │   ├── tools.py           # Agent tools for retrieval
│   │   └── verilens_agent.py  # Main VeriLens agent
│   ├── core/
│   │   └── config.py          # Central configuration management
│   ├── ingest/
│   │   ├── loader.py          # Document loading from disk
│   │   ├── pdf_loader.py      # PDF file processing
│   │   ├── chunker.py         # Text chunking with overlap
│   │   └── indexer.py         # Document indexing
│   ├── reason/
│   │   ├── generator.py       # Answer generation with LLM
│   │   └── prompt.py          # System prompts
│   ├── retrieve/
│   │   ├── embedder.py        # TF-IDF embeddings
│   │   ├── retriever.py       # Chunk retrieval
│   │   └── vector_store.py    # In-memory vector storage
│   ├── schemas/
│   │   ├── document.py        # Document and chunk models
│   │   ├── embedding.py       # Embedded chunk models
│   │   └── response.py        # Response schemas
│   └── verify/
│       ├── base.py            # Verification models
│       └── verifier.py        # Answer verification
```

## ✨ Features

- **PDF Support**: Load and process PDF documents with PyPDF2
- **Configurable Chunking**: Adjustable chunk size and overlap for optimal context retention
- **Groq Integration**: Leverages Llama 3.3 70B via Groq API for fast inference
- **TF-IDF Embeddings**: Efficient local embeddings without external API calls
- **Type Safety**: Built with Pydantic for robust data validation
- **Answer Verification**: Optional verification to ensure answers are grounded in evidence
- **Interactive CLI**: User-friendly command-line interface for document Q&A
- **Modular Design**: Clean separation of concerns for easy maintenance and extension

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- Groq API key (free at [console.groq.com](https://console.groq.com))

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/VERILENS.git
cd VERILENS
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
# or
source .venv/bin/activate  # Linux/Mac
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the root directory:
```env
GROQ_API_KEY=your_groq_api_key_here
```

### Configuration

The system can be configured via [app/core/core/config.py](app/core/core/config.py):

- `LLM_MODEL`: Language model for generation (default: llama-3.3-70b-versatile)
- `TOP_K`: Number of chunks to retrieve (default: 3)
- `CHUNK_SIZE`: Size of text chunks in characters (default: 500)
- `CHUNK_OVERLAP`: Overlap between consecutive chunks (default: 100)

## 📚 Usage

### Interactive Mode

Run the application and provide a PDF file:

```bash
python run.py
```

Then follow the prompts to:
1. Enter the path to your PDF file
2. Ask questions about the document
3. Get answers with source citations

### Programmatic Usage

```python
from app.core.ingest.pdf_loader import load_pdf
from app.core.ingest.chunker import chunk_document
from app.core.ingest.indexer import index_chunks
from app.core.retrieve.vector_store import VectorStore
from app.core.agent.verilens_agent import VeriLensAgent
from app.core.schemas.document import Document

# Load and process PDF
text = load_pdf("path/to/document.pdf")
document = Document(content=text, source="document.pdf")

# Chunk and index
vector_store = VectorStore()
chunks = chunk_document(document)
index_chunks(chunks, vector_store)

# Create agent and ask questions
agent = VeriLensAgent(vector_store)
answer = agent.answer("What is the main topic of this document?")
print(answer)
```

## 🛠️ Tech Stack

- **Pydantic**: Data validation and settings management
- **OpenAI SDK**: API client for Groq compatibility
- **Groq**: Fast LLM inference with Llama 3.3
- **NumPy**: Numerical operations
- **scikit-learn**: TF-IDF vectorization
- **PyPDF2**: PDF text extraction
- **scikit-learn**: Machine learning utilities
- **python-dotenv**: Environment variable management

## 📝 Project Status

Currently in active development. The core document processing pipeline is functional, with ongoing work on:
- Query processing
- Response generation
- Vector similarity search
- API endpoints

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues and pull requests.

## 📄 License

This project is open source and available under the MIT License.

---

**VERILENS** - Intelligent Document Processing and Retrieval
Contribution test
