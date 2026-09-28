import os
from groq import Groq
from memory_manager import HindsightMemoryManager
from dotenv import load_dotenv

load_dotenv()

class DealPilotAgent:
    def __init__(self):
        self.groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.memory = HindsightMemoryManager()
        # Official recommended models from hackathon brief
        self.primary_model = "qwen/qwen3-32b"
        self.fallback_model = "openai/gpt-oss-120b"

    def process_turn(self, bank_id: str, user_prompt: str, new_information: str = None):
        if new_information and new_information.strip():
            self.memory.retain(bank_id=bank_id, content=new_information.strip())

        recalled_memories = self.memory.recall(bank_id=bank_id, query=user_prompt)
        reflection = self.memory.reflect(
            bank_id=bank_id, 
            query="What are all non-negotiable buyer constraints, compliance clauses, and budget limits?"
        )

        memory_context = "\n".join([f"- {m}" for m in recalled_memories]) if recalled_memories else "No specific past context found."
        
        system_prompt = f"""You are DealPilot, an enterprise sales intelligence agent.
Your primary role is to ensure enterprise deals progress without violating past buyer constraints.

CRITICAL CLIENT MEMORY:
{memory_context}

STRATEGIC REFLECTION / GUARDRAILS:
{reflection}

INSTRUCTIONS:
1. Always adhere strictly to past constraints (pricing, compliance, subprocessors, billing terms).
2. Explicitly reference prior agreements when appropriate to demonstrate continuity.
3. Be professional, direct, and sales-ready.
"""

        # Resilient inference loop with fallback handling
        try:
            completion = self.groq_client.chat.completions.create(
                model=self.primary_model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.2
            )
            response_text = completion.choices[0].message.content
        except Exception as primary_err:
            print(f"[Primary Model Error with {self.primary_model}]: {primary_err}")
            print(f"Flipping to fallback model: {self.fallback_model}...")
            try:
                completion = self.groq_client.chat.completions.create(
                    model=self.fallback_model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    temperature=0.2
                )
                response_text = completion.choices[0].message.content
            except Exception as fallback_err:
                response_text = f"Agent encountered an execution error: {fallback_err}"

        return {
            "response": response_text,
            "recalled_memories": recalled_memories,
            "reflection": reflection
        }