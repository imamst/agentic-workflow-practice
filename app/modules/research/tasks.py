from weasyprint import HTML
from markdown import markdown
from app.modules.research.methods import generate_queries, generate_report, search_web


def research():
    queries = generate_queries(topic="Mobile Legends Bang Bang Draft Picks Strategy")

    research_context = ""

    for query in queries.queries:
        results = search_web(query)
        research_context += f"Query: {query}\nResults: {results}\n\n"

    research_result = generate_report(
        strategy="Pick off", research_context=research_context
    )

    result = markdown(text=research_result, output_format="html")
    HTML(string=result).write_pdf("output.pdf")


def research_task():
    research()
