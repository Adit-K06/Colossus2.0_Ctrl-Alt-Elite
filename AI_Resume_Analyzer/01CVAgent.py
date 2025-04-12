from dotenv import load_dotenv
load_dotenv()
import asyncio
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

# UI section
import streamlit as st

# UI Setup
st.title("💬 AI Interview Assistant")
st.caption("Powered by Gemini")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input handling
if prompt := st.chat_input("How can I help you today?"):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate response with error handling
    try:
        full_response = ""
        with st.spinner("Analyzing your question..."):
            with st.chat_message("assistant"):
                response_placeholder = st.empty()  # Create a placeholder
                response = cvReaderAgent.run(prompt, stream=True)
                for _resp_chunk in response:
                    # Display response
                    if _resp_chunk.content is not None:
                        full_response += _resp_chunk.content
                        response_placeholder.markdown(full_response.replace("%", "\\%") + "▌",
                                                      unsafe_allow_html=True)
                        response_placeholder.markdown(full_response.replace("%", "\\%"),
                                                  unsafe_allow_html=True)
        # Display assistant response
        st.session_state.messages.append({
            "role": "assistant",
            "content": full_response,
        })

    except Exception as e:
        st.error(f"Error generating response: {str(e)}")


