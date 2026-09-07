from llm.client import llm

response = llm.invoke("In one sentence, explain why stock research needs multiple resources")
print(response.content)
print(response.response_metadata)
print(response.usage_metadata)