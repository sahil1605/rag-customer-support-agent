from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from src.config import Config
from src.vector_store import VectorStore

class RAGAgent:
    def __init__(self):
        # Initialize Google Gemini model
        self.llm = ChatGoogleGenerativeAI(
            model=Config.GEMINI_MODEL,
            temperature=0.7,
            google_api_key=Config.GOOGLE_API_KEY
        )
        
        # Initialize Vector Store connection
        self.vector_store = VectorStore().get_db()
        
        # Define the system prompt
        self.prompt_template = ChatPromptTemplate.from_template("""
        You are a professional and helpful Customer Support Agent. 
        Your goal is to answer customer questions accurately and politely using the provided context.

        Guidelines:
        1. Use only the provided context to answer the question.
        2. If the answer is not in the context, politely inform the customer that you don't have that information and offer to escalate to a human agent.
        3. Do not make up facts.
        4. Keep your answers concise and relevant.

        Context:
        {context}

        Question:
        {question}

        Answer:
        """)

    def get_context(self, query, k=3):
        """Retrieves relevant chunks from the vector database."""
        docs = self.vector_store.similarity_search(query, k=k)
        return "\n\n".join([doc.page_content for doc in docs])

    def ask(self, question):
        """Orchestrates the retrieval and generation process."""
        # 1. Retrieve
        context = self.get_context(question)
        
        # 2. Augment & Generate
        chain = self.prompt_template | self.llm
        response = chain.invoke({
            "context": context,
            "question": question
        })
        
        return response.content

if __name__ == "__main__":
    # Quick test logic
    import sys
    import os
    sys.path.append(os.getcwd())
    
    agent = RAGAgent()
    test_query = "What is the return policy?"
    print(f"Query: {test_query}")
    print("-" * 30)
    print(agent.ask(test_query))
