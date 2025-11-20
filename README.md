# Ibase Chatbot - RAG-based PDF Q&A System

## Overview

Ibase Chatbot is a **Retrieval-Augmented Generation (RAG)** system that enables conversational Q&A over user-uploaded PDF documents. The system combines document processing, vector embeddings, semantic search, and large language models to provide accurate, context-aware answers.

## Architecture

```
User Upload PDF → Extract Text → Chunk Text → Generate Embeddings → Store in Vector DB
                                                                              ↓
User Query → Query Embedding → Semantic Search → Retrieve Relevant Chunks → LLM → Answer
```

## Key Components

### 1. **PDF Upload & Processing**
- Users upload PDF documents via web interface
- Extract text, tables, and metadata from PDFs
- Handle various PDF formats including scanned documents (OCR)

### 2. **Text Chunking**
- Split documents into manageable chunks (e.g., 500-1000 tokens)
- Preserve context with overlapping chunks
- Maintain document metadata for tracking

### 3. **Embedding Generation**
- Convert text chunks into vector embeddings
- Use models like OpenAI text-embedding-3-small or HuggingFace models
- Each chunk becomes a high-dimensional vector

### 4. **Vector Database Storage**
- Store embeddings in vector database (Pinecone, ChromaDB, Weaviate, FAISS)
- Index vectors for fast similarity search
- Link vectors to original text and metadata

### 5. **Retrieval System**
- Convert user query into embedding
- Perform semantic similarity search
- Retrieve top-k most relevant chunks

### 6. **LLM Response Generation**
- Pass retrieved chunks as context to LLM
- Generate grounded, conversational answers
- Cite sources from PDF documents

### 7. **Session Management**
- Track user sessions and uploads
- Store user-document associations
- Manage conversation history

## Technology Stack

### Frontend
- **React** - Modern web interface
- **Streamlit** - Quick prototyping dashboard

### Backend
- **Python** - Core application logic
- **FastAPI** - REST API server

### PDF Processing
- **PyMuPDF (fitz)** - PDF text extraction
- **pdfplumber** - Table extraction
- **pytesseract** - OCR for scanned PDFs

### Embeddings
- **OpenAI API** - text-embedding-3-small/large
- **HuggingFace Transformers** - Open-source models
- **Sentence Transformers** - all-MiniLM-L6-v2

### Vector Databases
- **Pinecone** - Managed vector DB
- **ChromaDB** - Lightweight local/hosted DB
- **Weaviate** - Open-source vector search
- **FAISS** - Facebook's similarity search library

### LLM
- **OpenAI GPT-4** - High-quality responses
- **GPT-3.5-turbo** - Cost-effective option
- **Claude** - Anthropic's models
- **Open-source LLMs** - Llama, Mistral, etc.

### Database
- **PostgreSQL** - User and session management
- **MongoDB** - Document metadata storage

## Installation

```bash
# Clone repository
git clone https://github.com/bsuraj23/ibase-chatbot.git
cd ibase-chatbot

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Configuration

Create `.env` file:

```env
OPENAI_API_KEY=your_openai_api_key
PINECONE_API_KEY=your_pinecone_api_key
PINECONE_ENVIRONMENT=your_pinecone_env
DATABASE_URL=postgresql://user:password@localhost/ibase_db
```

## Usage

### Running the Application

```bash
# Start the API server
python app.py

# Or with uvicorn
uvicorn app:app --reload --port 8000
```

### API Endpoints

#### Upload PDF
```bash
POST /upload
Content-Type: multipart/form-data
Body: {"file": pdf_file, "user_id": "user123"}
```

#### Query Chatbot
```bash
POST /query
Content-Type: application/json
Body: {
  "query": "What is the main topic?",
  "user_id": "user123",
  "session_id": "session456"
}
```

## Project Structure

```
ibase-chatbot/
├── app.py                  # Main FastAPI application
├── pdf_processor.py        # PDF extraction logic
├── embeddings.py          # Embedding generation
├── vector_db.py           # Vector database operations
├── retriever.py           # RAG retrieval logic
├── llm_interface.py       # LLM API integration
├── database.py            # Session/user management
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
└── README.md             # This file
```

## Pipeline Flow

### 1. Document Ingestion
```python
# User uploads PDF
PDF File → pdf_processor.extract_text()
         → pdf_processor.chunk_text()
         → embeddings.generate_embeddings()
         → vector_db.store_embeddings()
```

### 2. Query Processing
```python
# User asks question
Query → embeddings.generate_query_embedding()
      → vector_db.similarity_search()
      → retriever.get_context()
      → llm_interface.generate_answer()
      → Return answer with sources
```

## Features

✅ Multi-PDF support per user  
✅ Semantic search across documents  
✅ Source citation in answers  
✅ Conversation history tracking  
✅ OCR support for scanned PDFs  
✅ Scalable vector database  
✅ Session management  
✅ REST API interface  

## Future Enhancements

- [ ] Multi-language support
- [ ] Image/diagram extraction and analysis
- [ ] Document comparison features
- [ ] Fine-tuned embeddings for domain-specific use cases
- [ ] Real-time collaborative annotations
- [ ] Export conversation history
- [ ] Advanced filters (date, document type, etc.)

## Use Cases

- 📚 **Education**: Students querying textbooks and research papers
- 💼 **Enterprise**: Knowledge base for internal documents
- ⚖️ **Legal**: Contract analysis and legal document search
- 🏥 **Healthcare**: Medical literature search
- 📊 **Research**: Academic paper analysis

## Interview Demo Points

1. **System Design**: Explain RAG architecture and component interactions
2. **Scalability**: Discuss vector DB indexing and query optimization
3. **Trade-offs**: Embedding model selection, chunk size, retrieval strategy
4. **Production Concerns**: Rate limiting, caching, error handling
5. **Monitoring**: Track query latency, embedding costs, LLM token usage

## Contributing

Feel free to open issues or submit pull requests for improvements.

## License

MIT License

## Contact

Developed by **Suraj** - AI Engineer & Data Science Trainer  
GitHub: [@bsuraj23](https://github.com/bsuraj23)
