import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

oa_client = OpenAI(api_key=os.getenv("OPENROUTER_API_KEY"), base_url="https://openrouter.ai/api/v1")

# Simple Deep Research
# -> User Input a Topic
# -> Generate sets of queries to search the web
# -> Execute the queries and collect the results
# -> Summarize the results
# -> Generate a report of the results
