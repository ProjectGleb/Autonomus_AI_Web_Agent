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


user_goal = "navigate to the github website and create a new repository. For evey screenshot extract the key information and return it."
api_key = os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_MODEL_NAME"] = 'gpt-4-turbo'
warnings.filterwarnings("ignore")


###METHOD REQUIRES FOR THE USE OF _RUN ABSTRACT METHOD!
class OCR_Tool(BaseTool):
    name: str = "OCR TOOL"
    description: str = """This tool extracts and returns key information from a web-page's screenshot, as well as returning all of its interractive elements like buttons and text boxes.\n
    Args:\n
        - user_goal: Users goal as a string.\n
    Returns:\n
        - Key information extracted from the screenshot based on the user_goal.\n
        - Extracted interactive elements of a web-page, like buttons, and text boxes."""
    def _run(self, user_goal: str)->str:
        def encode_image(image_path):
            with open(image_path, "rb") as image_file:
                return base64.b64encode(image_file.read()).decode('utf-8')

        image_path = "/Users/gleb/Desktop/CS/Projects/AI_Web_Agent/Multi-Agent_Logic/Web_Screenshots/screenshot.jpg"

        base64_image = encode_image(image_path)

        # User's action
        # Prompt text with user's action
        prompt_text = f"""
        Role = Web-scraper \n
        Goal = You have two goals: 1. Extract the key information of the screenshot basede on the user_goal: {user_goal} and return it in the appropriate format (for example if the user asks to retrieve the key info from an email you should return only the emails contents). 2. Extract all the interactive elements (such as buttons and text boxes) seen on the screenshot and return them as a list of snake_casing_elements exactly like in this example: \n    
        example output = Interactive Elements: [accept_all_btn, accept_all_btn, accept_all_btn, github_signin_username_box, etc.]
        """

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }

        payload = {
            "model": "gpt-4o",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt_text
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ],
            "max_tokens": 400
        }

        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

        # Parse the JSON response to extract the useful content
        response_json = response.json()
        screenshot_content = response_json['choices'][0]['message']['content']

        # Access and print the specific parts of the response
        if 'choices' not in response_json:
            print("Error: No content found in the response.")
        return(screenshot_content)
    



ocr_result = OCR_Tool()

ocr_agent = Agent(
    role='OCR Analyzer',
    goal='Your role is to use the ocr_tool to extract key information from a screenshot of a webpage as well as all of its interactive elements and return it to the manager agent.',
    backstory='An OCR agent eager to help the managing agent extract the key elements in the web screenshot.',
    cache=True,
    verbose=True,
    tools=[ocr_result],
    allow_delegation=True
)

ocr_task = Task(
    description=(
        "1. Extract the key information of the screenshot based on the user_goal and return one screen element you think needs to be interracted with to achieve the user_goal.\n"),
    expected_output="Example output: youtube_login_btn.",
    agent=ocr_agent
)



# result = MyCustomTool()._run(user_goal)
# print(result)



# class OcrTool(BaseTool):
    # name: str = "Screenshot OCR Tool"
    # description: str = (
    #     "This function allows you to extract the browsers screenshots key information as well as any interactive elements like buttons and text boxes. "
    #     "It takes in an image path string as an argument. In this scenario, it is: '/Users/gleb/Desktop/CS/Projects/AI_Web_Agent/Autonomus_Logic/Web_Screenshots/screenshot.jpg'."
    # )

    # def _run(self):

    #     def encode_image(image_path):
    #         with open(image_path, "rb") as image_file:
    #             return base64.b64encode(image_file.read()).decode('utf-8')
            
    #     image_path = "/Users/gleb/Desktop/CS/Projects/AI_Web_Agent/Autonomus_Logic/Web_Screenshots/screenshot.jpg"
    #     base64_image = encode_image(image_path)

    #     user_goal = "navigate to the github website and create a new repository. For every screenshot extract the key information and return it."

    #     prompt_text = f"""
    #     You are a web-scraper. Your job is to extract information based on the screenshot of a webpage and user_action: {user_goal} and format it appropriately.
    #     In addition, describe what are the key interactive elements seen in this web page screenshot (such as buttons and text boxes) in the following format:
    #     interactive_elements = 
    #     'accept_all_btn',
    #     'google_search_box',
    #     'google_search_btn',
    #     'github_signin_username_box'
    #     """

    #     headers = {
    #         "Content-Type": "application/json",
    #         "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}"
    #     }

    #     payload = {
    #         "model": "gpt-4-turbo",
    #         "messages": [
    #             {
    #                 "role": "user",
    #                 "content": [
    #                     {
    #                         "type": "text",
    #                         "text": prompt_text
    #                     },
    #                     {
    #                         "type": "image",
    #                         "image": {
    #                             "url": f"data:image/jpeg;base64,{base64_image}"
    #                         }
    #                     }
    #                 ]
    #             }
    #         ],
    #         "max_tokens": 400
    #     }

    #     response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

    #     # Parse the JSON response to extract the useful content
    #     response_json = response.json()
    #     if 'choices' not in response_json:
    #         print("Error: No content found in the response.")
    #         return "Error: No content found in the response."

    #     screenshot_content = response_json['choices'][0]['message']['content']
    #     return screenshot_content






########## CREW WITH THE ABILITY TO UTILIZE THE OCR TOOL 

# planner = Agent(
#     role="Image Parser",
#     goal="Utilize your screenshot tool to take the image screenshot, extract the key information of the screenshot, and in a separate paragraph, retrieve the key interactive elements.",
#     backstory="You're an AI agent trying to help a user navigate the web-browser based on their query to achieve a specific goal by interacting with the browser.",
#     allow_delegation=False,
#     verbose=True,
#     tools=[ocr_tool]
# )



# plan = Task(
#     description=(
#         """After extracting the key info, return it along with the interactive elements in the following format:
#         interactive_elements = 
#         'accept_all_btn',
#         'google_search_box',
#         'google_search_btn',
#         'github_signin_username_box'.
#         """
#     ),
#     expected_output="Output: [element_btn1, element_btn2, element_textbox1, element_textbox2, etc.]",
#     agent=planner
# )


# crew = Crew(
#     agents=[planner],
#     tasks=[plan],
#     verbose=2,
# #     memory = True

# # )

# # past_actions = {'action_history': {'Click0': 'accept_browser_cookies_btn', 'Type0': "{google_search_box : github.com}"}}
# result = crew.kickoff()
