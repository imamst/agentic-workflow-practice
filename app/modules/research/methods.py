import json
from app.modules.research.prompt import REPORT_SYSTEM_PROMPT
from app.modules.research.schema import QueriesSchema
from app.utils.openai import oa_client
from app.utils.tavily import tavily_client


def generate_queries(topic: str) -> QueriesSchema:
    response = oa_client.chat.completions.parse(
        model="google/gemini-3-flash-preview",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant that generates sets of queries to search the web.",
            },
            {
                "role": "user",
                "content": f"Generate 2 queries to search the web for the topic: {topic}",
            },
        ],
        response_format=QueriesSchema,
    )

    if not response:
        raise Exception("Failed to generate queries")

    return QueriesSchema(**response.choices[0].message.parsed.model_dump())  # type: ignore


def search_web(query: str) -> str:
    results = tavily_client.search(
        query, search_depth="advanced", include_raw_content="markdown"
    )

    response = oa_client.chat.completions.parse(
        model="deepseek/deepseek-v3.2-exp",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant that summarizes the results of a web search.",
            },
            {
                "role": "user",
                "content": f"Summarize the results of the following web search: {json.dumps(results)}",
            },
        ],
        extra_body={"reasoning": {"enabled": True}},
    )

    return response.choices[0].message.content  # type: ignore


def generate_report(strategy: str, research_context: str) -> str:
    response = oa_client.chat.completions.parse(
        model="deepseek/deepseek-v3.2-exp",
        messages=[
            {
                "role": "system",
                "content": REPORT_SYSTEM_PROMPT.format(
                    research_context=research_context
                ),
            },
            {"role": "user", "content": f"Strategy: {strategy}"},
        ],
        extra_body={"reasoning": {"enabled": True}},
    )

    return response.choices[0].message.content  # type: ignore
