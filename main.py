from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser

import os
from dotenv import load_dotenv

load_dotenv()  # read .env variable

MODEL_NAME  =   os.getenv("MODEL_NAME")
TEMPERATURE =   float(os.getenv("TEMPERATURE","0.5"))
MAX_TURNS =     int(os.getenv("MAX_TURNS","5"))

llm = ChatOllama(
    model=MODEL_NAME,
    temperature=0.7
)

# messages = [
#    SystemMessage(content="You are a helpful assistant that translates English to French. Translate the user sentence."),
#    HumanMessage(content="I love programming.")   
# ]

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful AI Assistant"),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human","{question}")
])

chain = prompt | llm | StrOutputParser()

chat_history = []  # Memory Store
# max_turns = 10  # 20 messages (Human + AI)

def chat(question):
    current_turn = len(chat_history) // 2

    if current_turn >= MAX_TURNS:
        return (
            "Context Window is full!"
            "The AI maynot follow the previous thread properly"
            "Please type 'clear to clear the context and start a new thread"
        )

    response = chain.invoke({
            "question": question,
            "chat_history": chat_history
    })

    chat_history.append(HumanMessage(content=question))
    chat_history.append(AIMessage(content=response))

    remaining = MAX_TURNS - (current_turn + 1)
    if remaining <= 2:
        response += f"Warning: Only {remaining} turn(s) left"

    return response

def main():
    print("LangChain ChatBot Ready! (Type 'quit' for exit, 'clear' for reset chat history)")
    
    while True:
        user_input = input("You: ").strip()

        if not user_input:
            continue
        if user_input.lower() == "quit":
            break
        if user_input.lower() == "clear":
            chat_history.clear()
            print("History cleared, Starting Fresh!")
            continue
        
        print(f"AI: {chat(user_input)}") 

main()

# print(chat("What is RAG?"))
# print(chat("Give me a python example of it"))
# print(chat("Now explain the code you just gave"))


# response = chain.invoke({"question":"What is RAG?"})
# print(response)

# for chunk in chain.stream({
#     "question":"What is RAG?",
#     "chat_history": chat_history
# }):
#     print(chunk, end="", flush=True)