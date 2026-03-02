# Simple Deep Research
# -> User Input a Topic
# -> Generate sets of queries to search the web
# -> Execute the queries and collect the results
# -> Summarize the results
# -> Generate a report of the results
from app.methods import generate_queries

def main():
    queries = generate_queries(topic="AI")
    print(queries.queries)


if __name__ == "__main__": # to prevent the code from being executed when the module is imported
    main()