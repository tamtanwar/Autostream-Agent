class AgentMemory:
    def __init__(self):
        self.name = None
        self.email = None
        self.platform = None
        self.current_step = None      # None, 'name', 'email', 'platform'
        self.last_intent = None       # tracks last high-level intent
        self.last_question = None     # tracks last RAG question
        self.in_lead_flow = False     # NEW: tracks if we are currently capturing lead