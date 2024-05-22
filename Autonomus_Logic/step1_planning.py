#Getting user input, and making a plan
from openai import OpenAI
from dotenv import load_dotenv
import json
import os
import requests
load_dotenv()
from step0_user_goal import get_user_input

user_goal = get_user_input()

def agent_planning(user_goal):
    # activate chatGPT agent
    import os

    api_key = os.getenv("OPENAI_API_KEY")

    url = "https://api.openai.com/v1/chat/completions"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    data = {
        "model": "gpt-4-turbo",
        "messages": [
            {
                "role": "system",
                "content": """You are a web agent, designed to craft a plan to achieve the user's goal which a computer will then execute. The plan should detail EVERY SINGLE click, type or other interaction a computer needs to take to navigate through the web browser to achieve the user's goal. The plan should be outputing each step as concrete actions like "Click", "Enter" "Scrawl", "Return", etc. Dont add conclusions.(Assume google.com is already opened). You are not limited to the number of steps you should take.
                As an example, if the user's request is "Tell me if there is anything important in my email inbox," here is the plan and format you should craft would look like this:
                PLAN: 1. Search :
                1. Type in search gmail.com in the search box.
                2. Click on the search button.
                3. Click on the first link.
                4. Type in email and password.
                5. Click on the sign in button.
                6. Click on the inbox.
                7. Read the first email.
                8. Extract the important information.
                9. Repeat step 5-9 for any unread emails.
                10. Return the important information to the user.
                11. End.
                 """

            },
            {
                "role": "user",
                "content": f"user goal:{user_goal}"
            }
        ]
    }

    response = requests.post(url, headers=headers, json=data)

    # Check if the request was successful
    if response.status_code == 200:
        # print("Response from OpenAI:", response.json())
        # print('\n')
        print(response.json()['choices'][0]['message']['content'])
    else:
        print("Error:", response.status_code, response.text)


agent_planning(user_goal)

