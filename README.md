# AutoStream Conversational AI Agent

## Project Overview
AutoStream Agent is a conversational AI assistant built for a fictional SaaS product, **AutoStream**, which provides automated video editing tools for content creators.  
The agent uses a local LLM (GPT4All) combined with a **Retrieval-Augmented Generation (RAG)** pipeline to answer product questions, identify high-intent users, and capture leads.

The agent can:  
1. Understand user intent dynamically (greeting, pricing inquiry, high-intent, polite messages).  
2. Answer product and pricing questions accurately using a local knowledge base.  
3. Detect high-intent users and collect lead information.  
4. Trigger backend actions (mock API) after lead information is collected.

---

## Features

- **Greeting & Polite Responses**: Handles greetings like `hi`, `hello`, `hey` and polite responses such as `thanks` or `okay`.  
- **Pricing/Product Inquiry (RAG + LLM)**: Uses a local JSON/Markdown knowledge base to answer questions about plans, pricing, and company policies.  
- **High-Intent Lead Capture**: Collects Name, Email, and Platform from the user and triggers `mock_lead_capture`.  
- **Fallback Handling**: Provides a default message when input is unrecognized.  
- **Offline & Free**: Entirely local, no paid API calls required.

---

## Folder Structure

## Folder Structure

```text
autostream-agent/
├── app/
│   ├── agent.py        # Main conversational agent logic
│   ├── intent.py       # AI-based intent detection
│   ├── memory.py       # Conversation memory & lead tracking
│   ├── tools.py        # Mock lead capture utilities
│   └── rag.py          # RAG setup for knowledge retrieval
│
├── knowledge_base.json # Local knowledge base used for RAG
├── main.py             # App entry point
├── requirements.txt    # Python dependencies
├── README.md           # Project documentation
└── .gitignore          # Git ignore rules (models, venv, cache)
```

---

## Setup Instructions

1. Clone the repository:

git clone 
cd autostream-agent

2. Create a virtual environment (optional but recommended):

python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows

3. Install dependencies:

pip install -r requirements.txt

4. Ensure the GPT4All model (e.g., `orca-mini-3b-gguf2-q4_0.gguf`) is downloaded and placed in the project folder.

5. Run the agent:

python main.py

6. Interact with the agent in the terminal. Type `'exit'` to quit.

---

## Architecture Explanation 

The AutoStream Agent combines **RAG (Retrieval-Augmented Generation)** with a local LLM (GPT4All) to deliver context-aware answers.  
The knowledge base, stored as a local JSON file, contains product plans, features, and company policies. A **vector store** is created using `faiss-cpu` and `sentence-transformers` to generate embeddings and enable similarity search for relevant content.  

The conversation flow is managed via a **memory class** (`AgentMemory`) which tracks lead capture steps, last intent, last question, and conversation history. This ensures that user inputs like confirmations (`yes`) or lead information are handled in context.  

Intent detection is hybrid: **keywords** handle simple greetings and polite messages, while GPT4All dynamically classifies more complex inputs into pricing inquiries, high-intent leads, or fallback.  

When a high-intent user is detected, the agent collects Name, Email, and Platform in sequence, and triggers the mock `lead_capture` function only after all information is obtained. The fallback mechanism ensures unrecognized queries receive a clear default message.  

This design ensures a **free, offline, assignment-ready agent** capable of demonstrating RAG, intent detection, lead capture, and polite conversational behavior.

---

## WhatsApp Deployment (Optional)

To deploy the agent on WhatsApp:

1. Use **WhatsApp Cloud API** or **Twilio WhatsApp API**.  
2. Create a webhook endpoint on your server that receives messages.  
3. Forward the messages to the `run_agent(user_input, vectorstore)` function.  
4. Return the agent’s response to WhatsApp through the API.  
5. Maintain **session memory per user** for multi-turn conversations.  

> Note: This is optional; the architecture allows seamless integration without changing core logic.

---

## Demo Flow (Generic)

1. **Greeting**:

User: hi
Agent: Hey 👋 I’m AutoStream. Wanna know about pricing or features?

2. **Pricing Inquiry**:

User: what are the plans
Agent: AutoStream Basic Plan costs $29/month… Pro Plan costs $79/month…

3. **High-Intent Lead Capture**:

User: i want pro
Agent: Nice 😄 What’s your name?
User: [User provides Name]
Agent: Cool. Drop your email 📧
User: [User provides Email]
Agent: Which platform do you create on? (YouTube, Instagram, etc.)
User: [User provides Platform]
🔥 LEAD CAPTURED 🔥
Agent: You’re all set 🚀 Our team will reach out shortly.

4. **Polite Response**:

User: thanks
Agent: You’re welcome! Let me know if you want to explore any other plans 🙂

---

## Notes

- The project is **completely free and offline**.  
- Fully demonstrates **RAG, intent detection, lead capture, polite handling, and fallback**.  
- Knowledge base can be extended without changing core code.  

---

## Author

**Tamanna**  
AutoStream Conversational AI Assignment


