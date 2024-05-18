Hey, this is an agent aiming to reinvent task automation. 

1. It takes a scribe recording of the desktop
    1.1 What are my options? Scribe doesnt have an api, meaning I likely have to manually trigger it every time through:
        web-scraping scirpt triggering scribe recording and then manually downloading the recoding after
    2. Create my own screenshotting software to take screenshots of the scibte 

2. Feeds it into Claud
3. Claud creates a breakdown of the UI elements in each screenshot and creates a readable format for AgenQL to execute upon
4. Agent QL then executes upon these descriptions

"How to safely store an api key"
from dotenv import load_dotenv
load_dotenv()
import os
KEY = os.environ["AGENTQL_API_KEY"]


"creating a conda env ""
conda create -n agent_env

 history 
 "for displaying command history"