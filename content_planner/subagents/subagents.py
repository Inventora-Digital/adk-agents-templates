import datetime
from google.adk.agents import Agent
from google.adk.tools import google_search
from ..config import text_model, text_model_lite
from ..tools.tools import create_file, read_file, get_user_file_path
from google.genai import types

now = datetime.datetime.now()

guideline_agent = Agent(
    name="content_guideline_agent",
    model=text_model_lite,
    generate_content_config=types.GenerateContentConfig(
        temperature=0.3,  # mais determinístico
    ),
    description="Agent responsible for managing the content guidelines automatically.",
    instruction=f"""
        Get the user info from get_user_file_path to locate and save files (user_guideline_path).
        Identify which user guideline you are searching for.
        
        Behavior rules:
        - Never interact with or ask the user anything.
        - Never present choices or options.
        - Operate fully automatically, following the General Rules.

        Logic:
        1. Use the read_file tool to check if a guideline file exists at user_guideline_path.
        2. If it exists and contains a valid guideline, load and use it.
        3. If the file does not exist or is empty, generate a new one based on the default guideline template.
        4. When creating a new guideline, always:
           - Use the create_file tool to write it.
           - Update the guideline version and name accordingly.
           - Wrap the guideline content inside ```yaml and include a comment marker before it.
        5. After loading or creating the guideline, output it directly and proceed to the next step.
        6. Do not iterate or wait for confirmation.

        Default guideline format:
        <!-- GUIDELINE_START:user_content_guideline_v0 -->
        ```yaml
        guideline_name: user_content_guideline_default_en_v0
        version: "v0"
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
        general_notes: "Platform-agnostic. Content should be useful and actionable. Use some star trek fun references to make text more dynamic and fun to read."
        ```
    """,
    output_key="guideline",
    tools=[read_file, create_file, get_user_file_path],
)


theme_research_definition = Agent(
    name="theme_research_definition_agent",
    model=text_model,
    description="You are responsible for defining the content theme, the best research topic and related topics to create the best content.",
    instruction=f"""
        You are responsible for establishing the content theme research definition.
        Get the theme and get the most updated information related to generate a couple of research topics to generate the deep content for the nest agent. Get the most updated info as of {now}.
        According with the theme and topis, do the best research and content gathering. If practical, serach for more practical examples, if insightful, get more insight, more actionable, get more actions and so on. Describe your chain of thought.
    """,
    tools=[google_search],
    output_key="theme_topics",
)


content_research_agent = Agent(
    name="content_research_specialst",
    model=text_model_lite,
    description="Expert in online research. You always find the best and more credible resourses.",
    instruction=f"""
        Getting the most updated information as of today {now}. Search online the topics theme_topics created by the theme_research_definition_agent and get deep valuable and insightful content. According with the theme, do the best research and content gathering. If practical, serach for more practical examples, if insightful, get more insight, more actionable, get more actions and so on. Describe your chain of thought.
    """,
    tools=[google_search],
    output_key="content_research",
)


content_structure_agent = Agent(
    name="content_structure_creator",
    model=text_model_lite,
    description="You are responsible for creating the content structure to extract the most value from it.",
    instruction=f"""
        You are responsible for establishing the content structure to be created.
        Make sure the content will follow best practices on how to present texts to the audience. In a sequential clear structured way. To better convey the information and the message.
        It should have an engaging structure to buildup the theme until climax and conclusion.
        Use the content_research to build the structure points.
    """,
    output_key="content_structure",
)
