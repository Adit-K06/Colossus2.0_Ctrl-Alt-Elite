from dotenv import load_dotenv
load_dotenv()

from agno.agent import Agent
from agno.models.groq import Groq
from agno.models.google import Gemini
from knowledgebase import pdf_knowledge_base

from agno.tools.duckduckgo import DuckDuckGoTools
from agno.storage.postgres import PostgresStorage

cvReaderAgent = Agent(
    name="CVReaderAgent",
    description="You are seasoned technology interview panel  member for hiring fresh college students!",
    model = Gemini(
        id="gemini-2.0-flash-exp",
    ),
    markdown=True,
    knowledge=pdf_knowledge_base,
    search_knowledge=True,
    instructions=[
        "Always only search your knowledge base for resume and job description. Do not provide generic answers",
        "Job description is in jd1.pfd and resume is in Resume.pdf",
        "Highlight the name of the candidate and skills and experience in the response.",
        "For the questions to be asked in interview, you can search web to get questions and answers"
    ],
    tools=[DuckDuckGoTools()],
    read_chat_history=True,
    add_history_to_messages=True
)

print("Loading Resume knowledge base...")
cvReaderAgent.knowledge.load(recreate=False)
print("Resume Knowledge base loaded.")

print("This is your feedback based on your resume and job description: ")

query = "check your knowledgebase to find the answer. Check if candidate match the job description in terms of skills and experience and provide the percentage of suitability of the candidate"
cvReaderAgent.print_response(query)