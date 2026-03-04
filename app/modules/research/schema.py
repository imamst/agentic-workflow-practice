from pydantic import BaseModel, Field


class QueriesSchema(BaseModel):
    queries: list[str] = Field(
        description="A list of queries to search the web for the topic"
    )


class ResearchInput(BaseModel):
    topic: str = Field(description="The topic of the research")
