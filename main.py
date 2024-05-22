import agentql
import time
from playwright.sync_api import sync_playwright
import json
from dotenv import load_dotenv
import os
load_dotenv()

'''
1. GOAL (create github repo) √
2. CONSTRUCT A STEP BY STEP PLAN 
3. TRANSCRIBE THE SCREENSHOT {outline interactive elements} √
    3.2 SAVE TO MEMORY
4.1 CHECK ACTION MEMORY,
    4.2  MAKE 1 ACTION PLAN
5. EXECUTE (USE AGENTQL)
6. SAVE TO MEMORY {goal, action, outcome}

'''


# Agent = LLM + memory(?) + planning skills(PDF?) + tool use(AgentQL)
session = agentql.start_session("https://www.google.com")

time.sleep(1)

session.current_page.screenshot(path='screenshot.png')
time.sleep(1)


session.stop()
