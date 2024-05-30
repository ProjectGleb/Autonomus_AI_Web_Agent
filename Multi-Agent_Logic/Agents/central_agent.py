from langchain_openai import ChatOpenAI
from crewai import Crew, Process, Agent
from dotenv import load_dotenv
import os
import warnings
from crewai import Agent, Task, Crew
from ocr_agent import OCR_Tool, ocr_agent, ocr_task
from planning_agent import planner, plan 
user_goal = "user goal : navigate to the github website and create a new repository based on the current context. Do it step by step stearting from the current screens context"
api_key = os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_MODEL_NAME"] = 'gpt-4-turbo'


warnings.filterwarnings("ignore")

project_crew = Crew(
    tasks=[plan, ocr_task],
    agents=[planner, ocr_agent],
    manager_llm=ChatOpenAI(temperature=0, model="gpt-4"),  # Mandatory for hierarchical process
    process=Process.hierarchical,  # Specifies the hierarchical management approach
    memory=True,  # Enable memory usage for enhanced task execution
)

#kickoff the crew
result = project_crew.kickoff(inputs={"user_goal": "USER GOAL: 'The user wants to create a new repository on Github'.",
                                      "past_actions":"PAST ACTIONS [Click0: accept_browser_cookies_btn, Type: {{google_search_box : github.com}}, Click1: github_link_btn, Type1: {{github_username_box : Gleb}}, Type2: {{github_password_box : 123}, ERROR ENCOUNTERED: AUTHENTICATION REQUIRED, CODE SENT TO gleb.studios@gmail.com]}", })

