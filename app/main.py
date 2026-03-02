# Simple Deep Research
# -> User Input a Topic
# -> Generate sets of queries to search the web
# -> Execute the queries and collect the results
# -> Summarize the results
# -> Generate a report of the results
from app.methods import generate_queries, search_web

def main():
    queries = generate_queries(topic="Mobile Legends Bang Bang Draft Picks")

    research_context = ""

    for query in queries.queries:
        results = search_web(query)
        research_context += f"Query: {query}\nResults: {results}\n\n"
    
    print(research_context)
    with open("research_context.txt", "w") as f:
        f.write(research_context)

if __name__ == "__main__": # to prevent the code from being executed when the module is imported
    main()