from tavily.tavily import TavilyClient
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

oa_client = OpenAI(api_key=os.getenv("OPENROUTER_API_KEY"), base_url="https://openrouter.ai/api/v1")

tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))