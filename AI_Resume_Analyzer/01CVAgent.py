from dotenv import load_dotenv
load_dotenv()

from agno.agent import Agent
from agno.models.groq import Groq
from knowledgebase import pdf_knowledge_base

from agno.tools.duckduckgo import DuckDuckGoTools
from agno.storage.postgres import PostgresStorage

cvReaderAgent = Agent(
    name="CVReaderAgent",
    description="You are seasoned technology interview panel  member for hiring fresh college students!",
    model = Groq(
        id="llama-3.3-70b-versatile",
    ),
    markdown=True,
    knowledge=pdf_knowledge_base,
    search_knowledge=True,
    instructions=[
        "Always only search your knowledge base for resumes. Do not provide generic answers",
        "Highlight the name of the candidate and skills and experience in the response.",
        "For the questions to be asked in interview, you can search web to get questions and answers"
    ],
    tools=[DuckDuckGoTools()],

)


print("Loading knowledge base...")
cvReaderAgent.knowledge.load(recreate=False)
print("Knowledge base loaded.")

query = "start"

while query.lower() != "exit":
    query = input("Enter your query: ")
    cvReaderAgent.print_response(query)

print('Bye....')
