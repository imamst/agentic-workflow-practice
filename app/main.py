# Simple Deep Research
# -> User Input a Topic
# -> Generate sets of queries to search the web
# -> Execute the queries and collect the results
# -> Summarize the results
# -> Generate a report of the results
from weasyprint import HTML
from markdown import markdown

from app.methods import generate_queries, search_web, generate_report

def main():
    queries = generate_queries(topic="Mobile Legends Bang Bang Draft Picks")

    research_context = ""

    for query in queries.queries:
        results = search_web(query)
        research_context += f"Query: {query}\nResults: {results}\n\n"
    
    research_result = generate_report(topic="Mobile Legends Bang Bang Draft Picks", research_context=research_context)

    result = markdown(text=research_result, output_format="html")
    HTML(string=result).write_pdf("output.pdf")

if __name__ == "__main__": # to prevent the code from being executed when the module is imported
    main()