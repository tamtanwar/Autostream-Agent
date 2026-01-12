import warnings

# Suppress deprecation and future warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=FutureWarning)
from app.rag import setup_rag
from app.agent import run_agent

vectorstore = setup_rag()

print("🤖 AutoStream Agent is live. Type 'exit' to quit.\n")

while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":
        break

    response = run_agent(user_input, vectorstore)
    print("Agent:", response)