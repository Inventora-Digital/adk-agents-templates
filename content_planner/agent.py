import datetime
from google.adk.agents import Agent
from .config import (
  text_model,
  text_model_lite
)
from .subagents.subagents import (
  content_planner_agent,
  response_formatter_agent
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

      Expected input:
        "content_theme": "<string>",
        "content_goal": "<string>",
        "target_audience": "<string>"
        "user_name": "<string>",
        "user_email": "<string>",
        "platforms": "optional<list>" - Default as article (web)

      Then, use the response_formatter_agent to format the output and use the final output as you final response. No aditional text needed.
    """,
    sub_agents=[
        content_planner_agent,
        response_formatter_agent
    ],
)
