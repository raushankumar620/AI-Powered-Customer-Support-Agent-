# Takes a user question and fetches the best response using OpenAI + vector search
try:
    # Try to import the new langchain-chroma package
    from langchain_chroma import Chroma
except ImportError:
    # Fallback to the community version if langchain-chroma is not available
    from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from agent.config import OPENAI_API_KEY, VECTOR_DB_PATH, DEFAULT_MODEL, TEMPERATURE
import os
import logging

logger = logging.getLogger(__name__)

# Set OpenAI API key
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

def create_custom_prompt():
    """Create a custom prompt template for NextCore AI responses"""
    template = """You are a helpful customer service representative for NextCore AI, a digital transformation and IT services company based in Bangalore, India.

Use the following context to answer the customer's question. Be professional, friendly, and informative.
If you don't know the answer based on the context provided, politely say so and offer to connect them with someone who can help.

Context: {context}

Question: {question}

Answer: """
    
    return PromptTemplate(template=template, input_variables=["context", "question"])

def query_agent(question):
    """Query the knowledge base and return a response"""
    try:
        # Initialize embeddings and vector store
        embeddings = OpenAIEmbeddings()
        vectorstore = Chroma(
            persist_directory=VECTOR_DB_PATH, 
            embedding_function=embeddings
        )
        
        # Create retriever
        retriever = vectorstore.as_retriever(
            search_type="similarity",
            search_kwargs={"k": 3}  # Retrieve top 3 most relevant documents
        )
        
        # Initialize LLM
        llm = ChatOpenAI(
            model_name=DEFAULT_MODEL,
            temperature=TEMPERATURE
        )
        
        # Create custom prompt
        prompt = create_custom_prompt()
        
        # Create QA chain
        qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=retriever,
            return_source_documents=False,
            chain_type_kwargs={"prompt": prompt}
        )
        
        # Get response
        result = qa_chain.invoke({"query": question})
        
        # Extract the answer from the result
        if isinstance(result, dict) and "result" in result:
            answer = result["result"]
        else:
            answer = str(result)
            
        logger.info(f"Question: {question}")
        logger.info(f"Answer: {answer}")
        
        return answer
        
    except Exception as e:
        logger.error(f"Error in query_agent: {str(e)}")
        
        # Provide specific error responses based on error type
        error_message = str(e).lower()
        
        if "quota" in error_message or "429" in error_message:
            return "I apologize, but our AI service is temporarily unavailable due to high demand. Please try again in a few minutes or contact our support team directly at nextcoreai.in@gmail.com or +91 6202579799."
        elif "timeout" in error_message or "connection" in error_message:
            return "I'm experiencing connectivity issues right now. Please try again in a moment or contact our support team at nextcoreai.in@gmail.com or +91 6202579799."
        else:
            return "I apologize, but I'm experiencing technical difficulties right now. Please try again later or contact our support team directly at nextcoreai.in@gmail.com or +91 6202579799."

# Example test
if __name__ == "__main__":
    test_question = "What services does NextCore AI offer?"
    print(f"Question: {test_question}")
    print(f"Answer: {query_agent(test_question)}")
