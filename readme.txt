Hey, this is multi-agent system aiming to automate digital labour. 

This agent has two funcitons:
1) Learning how to perform tasks trought a desktop recording tutorial (currently using scribe, but will soon use video looms!) 
2) Automatically figure out how to perform web tasks based on a text prompt.

The way it works is:
1)
1. Once you create a screen recording (using scribe or loom) it transcribes it using GPTv into actionable steps.
2. It parses it thorugh AgentQL which begins a browser sesssion, grabs retrieves web elements to be interacted with.
3. Interacts with the retrieved elements

2) 
1. Based on the text query the agent constructs a plan of how to accomplish the goal.
3. It begins the browser session and transcribes it's screenshots using GPTv
4. The transcription then gets parsed by the LLM into AgentQL Query that then interacts with the web-page.
5. The changing we-state then gets re-analyzed against the goal and the cycle begins again.
