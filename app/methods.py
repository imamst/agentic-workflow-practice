from app.utils import oa_client
from pydantic import BaseModel, Field

class QueriesSchema(BaseModel):
    queries: list[str] = Field(description="A list of queries to search the web for the topic")

def generate_queries(topic: str) -> QueriesSchema:
    response = oa_client.chat.completions.parse(
        model="google/gemini-3-flash-preview",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that generates sets of queries to search the web."},
            {"role": "user", "content": f"Generate 5 queries to search the web for the topic: {topic}"}
        ],
        response_format=QueriesSchema
    ) 

    if not response:
        raise Exception("Failed to generate queries")

    return QueriesSchema(**response.choices[0].message.parsed.model_dump()) # type: ignore