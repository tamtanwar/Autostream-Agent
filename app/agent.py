import warnings
from gpt4all import GPT4All
from app.intent import detect_intent
from app.tools import mock_lead_capture
from app.memory import AgentMemory

# ------------------------------
# Suppress warnings
# ------------------------------
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=FutureWarning)

# ------------------------------
# Initialize model & memory
# ------------------------------
model = GPT4All("orca-mini-3b-gguf2-q4_0.gguf")
memory = AgentMemory()
memory.conversation_history = []

# ------------------------------
# Run agent
# ------------------------------
def run_agent(user_input, vectorstore):
    user_text = user_input.strip()
    intent = detect_intent(user_text)

    # -------------------------
    # Greeting
    # -------------------------
    GREETING_KEYWORDS = ["hi", "hello", "hey", "heyyyy"]
    if user_text.lower() in GREETING_KEYWORDS or intent == "greeting":
        memory.last_intent = "greeting"
        reply = "Hey 👋 I’m AutoStream. Wanna know about pricing or features?"
        memory.conversation_history.append({"agent": reply})
        return reply

    # -------------------------
    # Lead capture flow
    # -------------------------
    if intent == "high_intent" and not memory.in_lead_flow:
        memory.in_lead_flow = True
        memory.current_step = "name"
        reply = "Nice 😄 What’s your name?"
        memory.conversation_history.append({"agent": reply})
        return reply

    if memory.in_lead_flow:
        if memory.current_step == "name":
            memory.name = user_text
            memory.current_step = "email"
            reply = "Cool. Drop your email 📧"
            memory.conversation_history.append({"agent": reply})
            return reply

        if memory.current_step == "email":
            memory.email = user_text
            memory.current_step = "platform"
            reply = "Which platform do you create on? (YouTube, Instagram, etc.)"
            memory.conversation_history.append({"agent": reply})
            return reply

        if memory.current_step == "platform":
            memory.platform = user_text
            memory.current_step = None
            memory.in_lead_flow = False
            mock_lead_capture(memory.name, memory.email, memory.platform)
            memory.last_intent = None
            memory.last_question = None
            reply = "You’re all set 🚀 Our team will reach out shortly."
            memory.conversation_history.append({"agent": reply})
            return reply

    # -------------------------
    # Pricing / Product Inquiry (RAG + LLM)
    # -------------------------
    if intent == "pricing" or (intent == "other" and memory.last_intent == "pricing"):
        memory.last_intent = "pricing"
        memory.last_question = user_text

        # Retrieve relevant docs from RAG
        docs = vectorstore.similarity_search(user_text, k=4)
        context_text = "\n".join([doc.page_content for doc in docs])

        # LLM prompt
        prompt = f"""
You are a friendly customer support assistant for AutoStream.
Answer the user's question using ONLY the information below.
Do NOT say 'I am an AI language model' or invent any facts.
If the answer is not in the information, say 'I don't know'.

Context:
{context_text}

Conversation history:
{memory.conversation_history}

User Question: {user_text}

Answer in full sentences as a helpful assistant:
"""
        response = model.generate(prompt)
        memory.conversation_history.append({"agent": response})
        return response

    # -------------------------
    # Polite / Thank-you messages
    # -------------------------
    POLITE_KEYWORDS = ["thanks", "thank you", "ok", "okay", "no thanks", "nah"]
    if user_text.lower() in POLITE_KEYWORDS or intent == "polite":
        reply = "You’re welcome! Let me know if you want to explore any other plans 🙂"
        memory.conversation_history.append({"agent": reply})
        return reply

    # -------------------------
    # Default fallback
    # -------------------------
    reply = "Oops! I didn't understand that. Please ask about plans or type 'hi' to start again."
    memory.conversation_history.append({"agent": reply})
    return reply