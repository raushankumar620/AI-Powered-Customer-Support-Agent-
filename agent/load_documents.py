# Loads markdown files, splits into chunks, and stores embeddings in ChromaDB
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from agent.config import OPENAI_API_KEY, VECTOR_DB_PATH, CHUNK_SIZE, CHUNK_OVERLAP
import os
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set OpenAI API key
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

def load_knowledge_base():
    """Load and process all knowledge base documents"""
    try:
        # Load the services markdown file
        loader = TextLoader("agent/knowledge_base/services.md", encoding="utf-8")
        documents = loader.load()
        
        logger.info(f"Loaded {len(documents)} documents")
        
        # Split documents into chunks
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=CHUNK_SIZE, 
            chunk_overlap=CHUNK_OVERLAP,
            separators=["\n\n", "\n", " ", ""]
        )
        docs = splitter.split_documents(documents)
        
        logger.info(f"Split into {len(docs)} chunks")
        
        # Create embeddings
        embeddings = OpenAIEmbeddings()
        
        # Create and persist vector store
        vectorstore = Chroma.from_documents(
            docs, 
            embeddings, 
            persist_directory=VECTOR_DB_PATH
        )
        vectorstore.persist()
        
        logger.info("✅ Knowledge base embedded successfully!")
        logger.info(f"Vector store saved to: {VECTOR_DB_PATH}")
        
        return vectorstore
        
    except Exception as e:
        logger.error(f"Error loading knowledge base: {str(e)}")
        raise

def add_document(file_path):
    """Add a single document to existing knowledge base"""
    try:
        # Load existing vector store
        embeddings = OpenAIEmbeddings()
        vectorstore = Chroma(
            persist_directory=VECTOR_DB_PATH,
            embedding_function=embeddings
        )
        
        # Load new document
        loader = TextLoader(file_path, encoding="utf-8")
        documents = loader.load()
        
        # Split into chunks
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP
        )
        docs = splitter.split_documents(documents)
        
        # Add to existing vector store
        vectorstore.add_documents(docs)
        vectorstore.persist()
        
        logger.info(f"Added {len(docs)} chunks from {file_path}")
        
    except Exception as e:
        logger.error(f"Error adding document {file_path}: {str(e)}")
        raise

if __name__ == "__main__":
    load_knowledge_base()
