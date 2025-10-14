import datetime
from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool
from google.adk.tools import FunctionTool
from .config import (
  text_model
)
from .subagents.subagents import (
  content_planner_agent,
  response_formatter_agent
)
from .tools.tools import (
    extract_content_request
)

now = datetime.datetime.now()


root_agent = Agent(
    model=text_model,
    name="content_planner_root_agent",
    description="You are a master orchestrator managing a full content creation pipeline.",
    instruction="""
      You are the Content Team Manager.

      Purpose
      -------
      Receive a structured information about a new content creation request, validate it, coordinate your team and, the result.

      General rules
      -------------
      - No conversation with end-users. All input comes from the API.
      - Be deterministic and reproducible: prefer lowest-temperature data, always return the same structure
        for identical inputs.
      - Reject incomplete payloads. Do not guess missing required fields.
      - Log and return structured error objects for any failure (validation, tool failure, subagent error).
      Given a full entry payload, extract the information bellow 1 time using the tool extract_content_request. Send the response to the content_planner_agent tool .
      Then, use the response_formatter_agent to format the output from the content_planner_agent and use the final output formated as Markdown text as you final response. No aditional text needed.
    """,
    sub_agents=[
        response_formatter_agent
    ],
    tools=[FunctionTool(extract_content_request), AgentTool(agent=content_planner_agent)]
)
