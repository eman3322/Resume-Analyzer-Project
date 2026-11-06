from services.llm import call_llm

result = call_llm('Return JSON like {"hello": "world"} and nothing else.')
print(result)