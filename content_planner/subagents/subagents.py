from google.adk.agents import Agent
from ..config import (text_model)
from ..tools.tools import (
    create_file,
    read_file,
    get_user_file_path
)
from google.genai import types

guideline_agent = Agent(
    name="content_guideline_agent",
    model=text_model,
    generate_content_config=types.GenerateContentConfig(
        temperature=0.5, # More deterministic output
    ),
    description="You are the agent responsible for managing the content guidelines.",
    instruction=f"""
        Get the user info from get_user_file_path to know were to search and save files (user_guideline_path).
        Identify witch user guidelines you are searching for.
        To save the guidelines use the result from tool get_user_file_path - user_guideline_path.
        Verify if there are existing guidelines using the read_file tool passing the user_guideline_path as the path.
        If there are no guideline inside the file or the file do not exist use default to start creating a new guideline with the user and use the tool create_file to save the new guideline. User name on file path need to be formated properly.
        If there are guidelines inside the file, present the user with the options and let they choose. If the user creates another guideline or update an existing one, append the new guideline inside the file using the create_file tool.
        If the user do not update an existing guideline do not use the create guideline tool (no update needed)
        
        The create_file tool accept only the content (guideline) as parameter and it should be in the format of the default guideline. and update the guidelive version, name and numer when creating a new one (don't forget to wrap in ```yaml to make reading better inside the file and add a comment before each guideline)

        Default guideline:
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
    Iterate the guidelines with the user before saving. 
    Always use the format of the template above to save future guidelines.
    Once guideline is created or saved, proceed to content creation.
    """,
    output_key="guideline",
    tools=[read_file, create_file, get_user_file_path]
)