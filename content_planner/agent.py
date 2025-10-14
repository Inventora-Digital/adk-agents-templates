import datetime
from google.adk.agents import Agent
from .config import text_model
from .config import text_model_lite
from .subagents.subagents import guideline_agent
from .subagents.subagents import content_structure_agent
from .subagents.subagents import theme_research_definition
from .subagents.subagents import content_research_agent
from .tools.tools import (
    get_user_list,
    create_user_list,
    get_user_file_path,
    create_file,
    read_file,
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
        "custom_fields": { ... }
    """,
    sub_agents=[
        guideline_agent,
        content_research_agent,
        content_structure_agent,
        theme_research_definition,
    ],
)
