from langchain_openai import ChatOpenAI
from crewai import Crew, Process, Agent, Task
from dotenv import load_dotenv
import os
import warnings
from ocr_agent import OCR_Tool, ocr_agent, ocr_task
from planning_agent import planner, plan


###How do I get the agent to run asyncronously?
#Try coppying the exisiting asyncronos code




async def _load_stuff():
    return await do_things()

 def _get_my_tool() -> Tool:
    return Tool(
        name="my tool name"
        func=lambda *args, **kwargs: print("***** NOT IMPLEMENTED*****"),
        coroutine=_load_stuff,
        description="a good description"
    )