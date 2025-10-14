from google.adk.models.lite_llm import LiteLlm
from dotenv import load_dotenv
import os

load_dotenv()
os.environ.setdefault("GOOGLE_GENAI_USE_VERTEXAI", "FALSE")
os.environ.setdefault("GOOGLE_CLOUD_PROJECT", "gen-lang-client-0626131813")
os.environ.setdefault("GOOGLE_CLOUD_REGION", "us-central1")
google_api_key = os.getenv("GOOGLE_API_KEY")

audio_model_native_audio = LiteLlm(
    model="gemini-live-2.5-flash-preview-native-audio", api_key=google_api_key
)
audio_model = LiteLlm(model="gemini-live-2.5-flash-preview", api_key=google_api_key)
text_model_lite = LiteLlm(model="gemini-2.5-flash-lite", api_key=google_api_key)
text_model = LiteLlm(model="gemini-2.5-flash", api_key=google_api_key)
image_model = LiteLlm(model="gemini-2.5-flash-image-preview", api_key=google_api_key)
