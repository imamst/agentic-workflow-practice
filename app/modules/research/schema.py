from pydantic import BaseModel, Field


class QueriesSchema(BaseModel):
    queries: list[str] = Field(
        description="A list of queries to search the web for the topic"
    )


class ResearchInput(BaseModel):
    strategy: str = Field(description="The MLBB draft strategy to research")
