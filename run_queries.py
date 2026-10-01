import json
import requests

queries = [
    "What does the retrieval endpoint return?",
    "How is the submission evaluated?",
    "Which LangChain text splitter is suggested for splitting the document?",
    "Is a public GitHub repository allowed?",
    "What must the README include?",
]

output = []
for q in queries:
    response = requests.post(
        "http://127.0.0.1:8000/query", json={"query": q, "top_k": 3}
    )
    output.append({"query": q, "results": response.json()})

with open("results.json", "w") as f:
    json.dump(output, f, indent=2)

print("results.json written")