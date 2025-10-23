from dotenv import load_dotenv
import os

#Load env variables
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

if not OPENAI_API_KEY:
    raise EnvironmentError("OPENAI_API_KEY not found. Create a .env file and add it.")