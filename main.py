import agentql
import time
from playwright.sync_api import sync_playwright
import json
from dotenv import load_dotenv
import os
load_dotenv()

'''
1. GOAL (create github repo)
2. CHECK MEMOORY {actions}, {plans}, {goals}
3. MAKE PLAN {1 action}
5. EXECTURE
6. SAVE TO MEMORY {goal, action, outcome}

'''


# Agent = LLM + memory(?) + planning skills(PDF?) + tool use(AgentQL)
session = agentql.start_session("https://www.google.com")

time.sleep(1)

session.current_page.screenshot(path='screenshot.png')
time.sleep(1)


session.stop()
