# Fallback query agent that works without OpenAI embeddings
import logging

logger = logging.getLogger(__name__)

# Fallback responses for common NextCore AI queries
FALLBACK_RESPONSES = {
    "services": """NextCore AI offers comprehensive digital transformation services including:
    
1. AI & Automation - Chatbots, RPA, AI consulting using Python, TensorFlow
2. Web Development - React, Node.js, Django websites and web applications
3. Mobile App Development - Flutter, React Native, iOS/Android apps
4. Cloud Services - AWS, Azure deployment, migration, and DevOps
5. UI/UX Design - Figma, Adobe XD design and prototyping
6. SEO & Content Writing - Organic traffic growth and content strategy
7. Ecommerce Development - Shopify, WooCommerce, custom stores
8. Graphic Design - Logos, branding, marketing materials

We're based in Bangalore and serve clients globally with full-stack teams.""",
    
    "technologies": """Our technology stack includes:
    
Frontend: React.js, Next.js, Vue.js, HTML5, CSS3, JavaScript
Backend: Node.js, Python, Django, Flask, PHP Laravel
Mobile: Flutter, React Native, Kotlin, Swift
Databases: MongoDB, MySQL, PostgreSQL, Firebase
Cloud: AWS, Azure, Google Cloud, DigitalOcean
AI/ML: OpenAI GPT-4, TensorFlow, PyTorch, LangChain
DevOps: Docker, Kubernetes, Jenkins, CI/CD pipelines""",
    
    "contact": """You can reach NextCore AI at:
    
Email: nextcoreai.in@gmail.com
Phone: +91 6202579799
Location: Bangalore, Karnataka, India

We're available for consultations and project discussions.""",
    
    "pricing": """Our pricing varies based on project scope and requirements. We offer:
    
- Competitive rates for all services
- Flexible engagement models
- Free initial consultations
- Transparent project estimates

Please contact us at nextcoreai.in@gmail.com or +91 6202579799 for a detailed quote.""",
    
    "about": """NextCore AI is a Bangalore-based digital transformation company offering cutting-edge technology solutions to startups, SMEs, and enterprises globally. 

We specialize in AI automation, web development, mobile apps, cloud services, and digital design. Our vision is to reshape the digital world through intelligent systems and scalable architectures."""
}

def query_agent_fallback(question: str) -> str:
    """
    Fallback query agent that works without OpenAI embeddings
    Uses keyword matching for common queries
    """
    try:
        question_lower = question.lower()
        
        # Check for service-related queries
        if any(word in question_lower for word in ["service", "offer", "do", "provide", "what"]):
            return FALLBACK_RESPONSES["services"]
        
        # Check for technology queries
        elif any(word in question_lower for word in ["technology", "tech", "stack", "tools", "framework"]):
            return FALLBACK_RESPONSES["technologies"]
        
        # Check for contact queries
        elif any(word in question_lower for word in ["contact", "reach", "phone", "email", "address"]):
            return FALLBACK_RESPONSES["contact"]
        
        # Check for pricing queries
        elif any(word in question_lower for word in ["price", "cost", "fee", "charge", "rate"]):
            return FALLBACK_RESPONSES["pricing"]
        
        # Check for about queries
        elif any(word in question_lower for word in ["about", "company", "who", "nextcore"]):
            return FALLBACK_RESPONSES["about"]
        
        # Default response
        else:
            return f"""Thank you for your question about "{question}". 

NextCore AI is a full-service digital transformation company based in Bangalore. We offer AI automation, web development, mobile apps, cloud services, UI/UX design, and more.

For detailed information about your specific needs, please contact us:
Email: nextcoreai.in@gmail.com
Phone: +91 6202579799

How else can I help you today?"""
            
    except Exception as e:
        logger.error(f"Error in fallback query agent: {str(e)}")
        return """I'm here to help you learn about NextCore AI's services. We're a Bangalore-based digital transformation company offering AI, web development, mobile apps, and cloud solutions. 

Please contact us at nextcoreai.in@gmail.com or +91 6202579799 for detailed assistance."""

# Try to use the real query agent, fallback if it fails
def query_agent(question: str) -> str:
    """
    Smart query agent with fallback capability
    """
    try:
        # Try to import and use the real query agent
        from agent.query_agent import query_agent as real_query_agent
        return real_query_agent(question)
    except Exception as e:
        logger.warning(f"Real query agent failed, using fallback: {str(e)}")
        return query_agent_fallback(question)
