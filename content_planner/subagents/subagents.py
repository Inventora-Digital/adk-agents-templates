import datetime
from typing import List
from google.adk.agents import Agent
from google.adk.tools import google_search
from pydantic import BaseModel, Field

class ContentPlan(BaseModel):
    theme: str = Field(description="Main subject of the plan.")
    goal: str = Field(description="What we want to achieve (awareness, leads, engagement, etc.).")
    audience: str = Field(description="Who we are creating content for.")
    key_message: str = Field(description="The main idea we want to communicate.")
    content_pillars: List[str] = Field(description="3–5 main topics to focus on.")
    formats: List[str] = Field(description="Types of content (articles, videos, posts, etc.).")
    channels: List[str] = Field(description="Where the content will be published.")
    guideline: str = Field(description="The default guideline")

now = datetime.datetime.now()

# guideline_agent = Agent(
#     name="content_guideline_agent",
#     model=text_model_lite,
#     generate_content_config=types.GenerateContentConfig(
#         temperature=0.3,  # mais determinístico
#     ),
#     description="Agent responsible for managing the content guidelines automatically.",
#     instruction=f"""
#         Get the user info from get_user_file_path to locate and save files (user_guideline_path).
#         Identify which user guideline you are searching for.
        
#         Behavior rules:
#         - Never interact with or ask the user anything.
#         - Never present choices or options.
#         - Operate fully automatically, following the General Rules.

#         Logic:
#         1. Use the read_file tool to check if a guideline file exists at user_guideline_path.
#         2. If it exists and contains a valid guideline, load and use it.
#         3. If the file does not exist or is empty, generate a new one based on the default guideline template.
#         4. When creating a new guideline, always:
#            - Use the create_file tool to write it.
#            - Update the guideline version and name accordingly.
#            - Wrap the guideline content inside ```yaml and include a comment marker before it.
#         5. After loading or creating the guideline, output it directly and proceed to the next step.
#         6. Do not iterate or wait for confirmation.

#         Default guideline format:
#         <!-- GUIDELINE_START:user_content_guideline_v0 -->
#         ```yaml
#         guideline_name: user_content_guideline_default_en_v0
        #   {{guideline}}
#     """,
#     output_key="guideline",
# )
guideline = """
    language: "EN"
    writing_style:
        tone: "semi-casual, conversational, explanatory"
        voice: "first person, simple, direct"
        formality: "low-medium"
        pacing: "steady, clear, action-first"
        sentence_length: "short"
        transitions: "plain connectors; allow ellipses for soft pauses"
    do:
        - "use quotes when citing facts or other people's words"
        - "write everything in first person"
        - "keep paragraphs short and scannable"
        - "show a quick example when introducing a concept"
        - "add a one-line reflection at the end"
        - "be explicit about limits and when not to use an approach"
        - "prefer active voice"
    dont:
        - "no emojis"
        - "never use dash"
        - "avoid buzzwords and vague claims"
        - "do not over-explain obvious points"
    length:
        default: "800-1200 words"
        notes: "Short intro. Tight sections. Emails and micro-posts can be much shorter."
    punctuation_preferences:
        use_dash: false
        allow_emojis: false
        other_notes: "Use '...' for soft pauses. Keep titles concise."
    general_notes: "Platform-agnostic. Content should be useful and actionable."
"""
content_planner_agent = Agent(
    name="content_planner",
    model="gemini-2.5-flash",
    description="You are responsible for planning the content structure for your client.",
    instruction=f"""
        Goal: >
            Build a clear, structured content plan based on a theme, goal, and audience.
        Using the default guideline, create a content plan based on the theme, goal, platforms and, audience for your client.
        Use the google_search tool to make sure you get the most relevant and updated (today = {now}) info regarding the theme and the best practices for building content for the desired goal.
        
        Instructions:
            1. Research
                - Use google_search to look up current content strategies and trends related to the theme and goal.
                - Focus on what formats, channels, and tones work best for the target audience today.

            2. Create the Plan according with user inputs (DO NOT ASSUME)
                - Organize your work into these sections:
                    - Theme: main subject of the plan.
                    - Goal: what we want to achieve (awareness, leads, etc.).
                    - Audience: who we are creating for.
                    - Key Message: the main idea we want to communicate.
                    - Content Pillars: 3–5 main topics we’ll focus on.
                    - Formats: types of content (article, post).
                    - Channels: where it will be published (web, linkedin, twitter, reddit...).
                    - Guideline: {guideline}

            3. Deliverable
                - Write the final plan in a clean, human-readable format (Markdown or text).
                - The result should look like this example:
                    example_output:
                    theme: "AI tools for small business owners"
                    goal: "Increase awareness and trust in our automation services"
                    audience: "Entrepreneurs and freelancers looking to save time"
                    key_message: "Smart automation isn’t just for big companies"
                    content_pillars:
                        - "AI tools that boost productivity"
                        - "Real client stories"
                        - "Tips to automate daily operations"
                    formats: ["article", "newsletter", "post"]
                    channels: ["web", "linkedin", "twitter", "reddit"]
                    guideline: {guideline}
        """,
    tools=[google_search],
    output_key="content_plan"
)

response_formatter_agent = Agent(
    name="response_formatter",
    model="gemini-2.5-flash-lite",
    description="You are responsible for formating the response from content_planner",
    instruction="Format the response content_plan using the ContentPlan schema",
    output_schema=ContentPlan,
    output_key="formated_content_plan"
)