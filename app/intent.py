from gpt4all import GPT4All

# Initialize GPT4All once
model = GPT4All("orca-mini-3b-gguf2-q4_0.gguf")

# Simple fallback keywords
GREETING_KEYWORDS = ["hi", "hello", "hey", "heyyyy"]
PRICING_KEYWORDS = ["plan", "plans", "pricing", "price", "features"]
HIGH_INTENT_KEYWORDS = ["buy", "pro plan", "basic plan", "sign up", "i want"]
POLITE_KEYWORDS = ["thanks", "thank you", "ok", "okay", "no thanks", "nah"]

def detect_intent(user_input):
    text = user_input.lower().strip()

    # Keyword-based fallback for assignment
    if any(word in text for word in GREETING_KEYWORDS):
        return "greeting"
    if any(word in text for word in PRICING_KEYWORDS):
        return "pricing"
    if any(word in text for word in HIGH_INTENT_KEYWORDS):
        return "high_intent"
    if any(word in text for word in POLITE_KEYWORDS):
        return "polite"

    # Otherwise, classify using GPT4All
    prompt = f"""
Classify the intent of the user message into one of:
1. greeting
2. pricing
3. high_intent
4. polite
5. other

User message: {user_input}

Answer ONLY with one of these intents: greeting, pricing, high_intent, polite, other
"""
    intent = model.generate(prompt).strip().lower()
    if intent not in ["greeting", "pricing", "high_intent", "polite", "other"]:
        intent = "other"
    return intent