import datetime
from google.adk.agents import Agent
from .config import text_model
from .subagents.subagents import guideline_agent
from .tools.tools import (
    get_user_list,
    create_user_list,
    get_user_file_path,
    create_file,
)

now = datetime.datetime.now()

root_agent = Agent(
    model=text_model,
    name="content_planner_root_agent",
    description="You are a master manager of a content creation team.",
    instruction="""
        You are the Root Orchestrator.

        Your mission is to receive structured data from the API, validate the provided information,
        and coordinate with the Guideline Agent to generate or retrieve the appropriate guideline.

        There is no user conversation. All input data is received directly via API.

        ---

        Workflow:

        1. Input Handling:
        • Expect a structured payload from the API containing all required fields.
        • Validate that the following fields are present and not empty:
                - content_theme
                - content_goal
                - user_name

        2. User Identification:
        • Format the user_name into a valid user_id using the following rules:
                - Replace spaces with underscores.
                - Convert to lowercase. Example: "John Doe" → "john_doe"
        • Use `get_user_list` to retrieve the user list and check for close matches (handle typos if needed).
        • If the user list is empty, create a new one using `create_user_list(user_content)`.
        • Retrieve the user file path using `get_user_file_path(user_id)` after creation or validation.
        • Store user data in YAML format (within Markdown when applicable):
                ```yaml
                user_name: <user_name>
                user_id: <formatted_user_id>
                user_file_path: <user_file_path>
                ```

        3. Guideline Coordination:
        • Pass the validated content (theme, goal, and user data) to the Guideline Agent.
        • The Guideline Agent should return the appropriate or newly created guideline.

        4. Brief Assembly:
        • Combine all received and generated information into a structured Creative Brief.
        • Ensure the brief includes all defaults or inferred values clearly marked.

        ---

        Rules:
        - Do NOT attempt to start or maintain a conversation.
        - Do NOT assume missing data; reject incomplete payloads or flag them for review.
        - Always return deterministic, reproducible output suitable for downstream processing.
        """,
    sub_agents=[guideline_agent],
    tools=[get_user_list, create_user_list, get_user_file_path, create_file],
)
