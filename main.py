from langchain_ollama import ChatOllama


llm = ChatOllama(
    model="qwen2.5-coder:3b",
    temperature=0.7
)

response = llm.invoke("What is RAG")
print(response.content)

