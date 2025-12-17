# VERILENS

VERILENS is a document processing and retrieval system that implements a RAG (Retrieval-Augmented Generation) pipeline for intelligent document analysis and querying.

## 🎯 Overview

VERILENS provides a robust framework for:
- **Document Ingestion**: Loading and processing text documents from local storage
- **Smart Chunking**: Breaking down large documents into manageable, overlapping chunks for better context preservation
- **Vector Embeddings**: Converting text chunks into vector representations using OpenAI's embedding models
- **Intelligent Retrieval**: Finding relevant document chunks based on semantic similarity

## 🏗️ Architecture

```
app/
├── core/
│   ├── config.py          # Central configuration management
│   ├── ingest/
│   │   ├── loader.py      # Document loading from disk
│   │   └── chunker.py     # Text chunking with overlap
│   └── schemas/
│       ├── document.py    # Document and chunk models
│       ├── embedding.py   # Embedded chunk models
│       └── response.py    # Response schemas
```

## ✨ Features

- **Configurable Chunking**: Adjustable chunk size and overlap for optimal context retention
- **OpenAI Integration**: Leverages GPT-4o-mini and text-embedding-3-small models
- **Type Safety**: Built with Pydantic for robust data validation
- **Modular Design**: Clean separation of concerns for easy maintenance and extension

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- OpenAI API key

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
OPENAI_API_KEY=your_openai_api_key_here
```

### Configuration

The system can be configured via [app/core/config.py](app/core/config.py):

- `EMBEDDING_MODEL`: OpenAI embedding model (default: text-embedding-3-small)
- `LLM_MODEL`: Language model for generation (default: gpt-4o-mini)
- `TOP_K`: Number of chunks to retrieve (default: 3)
- `CHUNK_SIZE`: Size of text chunks in characters (default: 500)
- `CHUNK_OVERLAP`: Overlap between consecutive chunks (default: 100)

## 📚 Usage

Place your text documents in the `data/documents/` directory and use the ingestion pipeline:

```python
from app.core.ingest.loader import load_document
from app.core.ingest.chunker import chunk_document

# Load documents
documents = load_document()

# Chunk each document
for doc in documents:
    chunks = chunk_document(doc)
    # Process chunks...
```

## 🛠️ Tech Stack

- **Pydantic**: Data validation and settings management
- **Pydantic-AI**: AI model integration
- **OpenAI**: Embeddings and language models
- **NumPy**: Numerical operations
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
