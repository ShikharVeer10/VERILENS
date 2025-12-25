"""
VERILENS - Document Q&A with Citations

A RAG-powered document analysis tool that provides answers 
with source citations from PDF documents.
"""

from app.core.ingest.pdf_loader import load_pdf
from app.core.ingest.chunker import chunk_document
from app.core.ingest.indexer import index_chunks
from app.core.retrieve.vector_store import VectorStore
from app.core.agent.verilens_agent import VeriLensAgent
from app.core.schemas.document import Document
import os
import sys


def print_banner():
    """Print the application banner."""
    print("\n" + "=" * 60)
    print("VERILENS - Document Q&A with Citations")
    print("=" * 60)
    print(" Powered by RAG (Retrieval-Augmented Generation)")
    print("-" * 60)


def get_pdf_path() -> str:
    """Get and validate the PDF file path from user."""
    while True:
        pdf_path = input("\nEnter the path to your PDF file: ").strip()
        pdf_path = pdf_path.strip('"').strip("'")
        
        if not pdf_path:
            print("   Please enter a valid path.")
            continue
            
        if os.path.exists(pdf_path):
            if pdf_path.lower().endswith('.pdf'):
                return pdf_path
            else:
                print("File must be a PDF. Please try again.")
        else:
            print(f" File not found: {pdf_path}")
            print("  Check the path and try again.")


def process_document(pdf_path: str) -> tuple:
    print(f"\nLoading: {os.path.basename(pdf_path)}", flush=True)
    vector_store = VectorStore()
    print(" Extracting text from PDF", end="", flush=True)
    text = load_pdf(pdf_path)
    print(" Done!", flush=True)
    
    if not text.strip():
        print("Warning: No text could be extracted from the PDF.")
        return None, None
    
    print(f"Extracted {len(text)} characters", flush=True)
    
    filename = os.path.basename(pdf_path)
    document = Document(content=text, source=filename)
  
    print("Chunking document", end="", flush=True)
    chunks = chunk_document(document)
    print(f" Done! Created {len(chunks)} chunks", flush=True)
   
    print("Indexing chunks", end="", flush=True)
    index_chunks(chunks, vector_store)
    print(" Done!", flush=True)
    
    print(f"Document ready for questions!", flush=True)
    
    return vector_store, filename


def run_qa_loop(agent: VeriLensAgent, document_name: str):
    print("\n" + "=" * 60)
    print(f" Document loaded: {document_name}")
    print("-" * 60)
    print(" Ask questions about your document.")
    print(" Commands:")
    print("  • Type your question and press Enter")
    print("  • Type 'exit' or 'quit' to end the session")
    print("  • Type 'new' to load a different document")
    print("=" * 60)
    
    while True:
        try:
            query = input("\n Your question: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\n\n Session ended. Thank you for using VERILENS!")
            return "exit"
        
        if not query:
            continue
            
        query_lower = query.lower()
        
        if query_lower in ('exit', 'quit', 'q'):
            print("\nThank you for using VERILENS!")
            return "exit"
        
        if query_lower == 'new':
            return "new"
        
        print("\n" + "─" * 50)
        print(" Answer:")
        print("─" * 50)
        
        try:
            answer = agent.answer(query)
            print(answer)
        except Exception as e:
            print(f" Error generating answer: {str(e)}")
            print("   Please try rephrasing your question.")
        
        print("─" * 50)


def main():
    """Main entry point for VERILENS."""
    print_banner()
    
    while True:
        # Get PDF path
        pdf_path = get_pdf_path()
        
        # Process document
        vector_store, filename = process_document(pdf_path)
        
        if vector_store is None:
            print("Failed to process document. Please try another file.")
            continue
        
        # Create agent
        agent = VeriLensAgent(vector_store)

        result = run_qa_loop(agent, filename)
        
        if result == "exit":
            break

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n Session interrupted. Goodbye!")
