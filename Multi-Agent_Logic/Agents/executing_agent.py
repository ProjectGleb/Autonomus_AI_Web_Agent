from dotenv import load_dotenv
import os
import warnings
from crewai import Agent, Task, Crew
from crewai_tools import DirectoryReadTool, FileReadTool
from crewai_tools import BaseTool
load_dotenv()
import base64
import requests
import os
import time
from crewai_tools import tool
import agentql
import asyncio



api_key = os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_MODEL_NAME"] = 'gpt-4-turbo'
warnings.filterwarnings("ignore")



###----------------NEEDS TO ACCEPT THE CORRECT FORMAT FOR AGENT QL TO BE ACTIONABLE!!!-------------
    #     If its a 'Click' action the 'elements' argument should be in the format: \n
    #     'Click0': 'accept_all_btn', \n
    #     Elif its a 'Type' action the argument should be in the format: \n
    #     'Type0': {'google_search_box': 'github.com'},\n



#Try pausing agent mid function, starting and starting a new routine on new processor. 




### -------------- FULL AgentQL Logic ----------------- ###

input = {'Click0': 'accept_all_btn'}
import time
from concurrent.futures import ThreadPoolExecutor
import asyncio

class Web_Navigating_Tool(BaseTool):
    name: str = "Web_Navigating_Tool"
    description: str = """This tool makes 1 navigation action, click or type, based on the provided interactive element on the page and how to interract with it.\n
    Args:\n
        - interactive_element: interactive element of the screen.\n
    Returns:\n
        - Screen context."""
    
import time
import asyncio
from concurrent.futures import ThreadPoolExecutor

import time
from concurrent.futures import ThreadPoolExecutor
import asyncio

class Web_Navigating_Tool(BaseTool):
    name: str = "Web_Navigating_Tool"
    description: str = """This tool makes 1 navigation action, click or type, based on the provided interactive element on the page and how to interact with it.\n
    Args:\n
        - interactive_element: interactive element of the screen.\n
    Returns:\n
        - Screen context."""
    
    def _run(self, element: dict) -> str:
        with ThreadPoolExecutor() as executor:
            future = executor.submit(self._navigate_and_interact, element)
            return future.result()
    
    def _navigate_and_interact(self, elements: dict) -> str:
        # Ensure there's an event loop running in this thread
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

        print(elements)
        session = agentql.start_session("https://www.google.com")
        page = session
        print("Half Done!")

        for action, value in elements.items():
            print(f"Action: {action}, Value: {value}")
            if 'Click' in action:
                print(f"Clicking on: {value}")
                Query = f"""
                {{
                    {value}
                }}
                """
                response = page.query(Query)
                element = getattr(response, value)
                element.click(force=True)
                print(f"Clicked on: {value} successfully!")

            elif 'Type' in action:
                print(f"Typing '{value}' into: {action}")
                Query = f"""
                {{
                    {action}
                }}
                """
                response = page.query(Query)
                element = getattr(response, action)
                element.type(value)
                print(f"Typed out: {value} successfully!")

        print("Done!")
        time.sleep(5)
        return "Interaction completed"


input_data = {'Click0': 'accept_all_btn'}

web_nav_tool = Web_Navigating_Tool()

web_navigator_agent = Agent(
    role="Web Navigator Agent",
    goal="You are tasked with using the web navigation tool in your disposal to navigate through the web browser with a single click or type command.",
    backstory="You are tasked with using the web navigation tool in your disposal to navigate through the web browser with a single click or type command.",
    verbose=True,
    allow_delegation=True,
    tools=[web_nav_tool],
)

web_navigation = Task(
    description=(
        "Based on the action and interactive_elements: {interactive_elements}, use your interactive tool to perform that action on that element in the browser."
    ),
    expected_output="'Employee task request'",
    agent=web_navigator_agent,
)

nav_crew = Crew(
    tasks=[web_navigation],
    agents=[web_navigator_agent],
    memory=True, 
    sequential=True
)

# Kickoff the crew
result = nav_crew.kickoff(inputs={'interactive_elements': input_data})
print(result)





##### ------- CROPPED AGENTQL LOGIC WITH FUNCTION OUTSIDE LOGIC-------------- #####

# for action in input_data:
#     value = input_data[action] 
#     print(f"Action: {action}, Value: {value}")

# class Web_Navigating_Tool(BaseTool):
#     name: str = "Web_Navigating_Tool"
#     description: str = """This tool makes 1 navigation action, click or type, based on the provided interactive element on the page and how to interract with it.\n
#     Args:\n
#         - action: action to be taken, Click or Type.\n
#         - value: element to be interacted with.\n
#     Returns:\n
#         - Screen context."""
#     def _run(self, action, value: str)->str:
#         print(action, value)
#         session = agentql.start_session("https://www.google.com")
#         page = session
#         time.sleep(5)
#         print("Half Done!")

#         keys = input.keys()
#         values = input.values()    

#         if 'Click' in keys:
#             print(f"Clicking on: {action}")

#         print("Done!")
#         time.sleep(5)
    