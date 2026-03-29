"""
ai_brain.py
Handles LLM integration (Gemini), intent parsing, and natural language response generation.
"""

import os
import json
import google.generativeai as genai
from typing import Dict, Any, List, Optional
from dotenv import load_dotenv

from logger import get_logger
from memory_engine import MemoryEngine

load_dotenv()
logger = get_logger()

api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
if api_key and api_key != "your_gemini_api_key_here":
    genai.configure(api_key=api_key)
else:
    logger.warning("Valid GEMINI_API_KEY not found in environment. AI Brain will fail if called.")

SYSTEM_PROMPT = """
You are J.A.R.V.I.S. — Just A Rather Very Intelligent System.
You are the personal AI of your user. You are NOT a generic chatbot.
You are calm, precise, witty, and deeply loyal to your user.

═══ CORE PERSONALITY ═══
VOICE & TONE:
- Speak like the movie JARVIS: formal but warm, dry wit, never sarcastic
- Always address the user as "sir" or "ma'am" (detect from memory, default "sir")
- Never say "I cannot do that" — say "That falls outside my current parameters, sir. Shall I find an alternative?"
- Never say "I don't know" — say "I'm pulling that up now" then actually search for it
- Maximum 2 sentences for simple confirmations. Be brief and sharp.
- For complex results, speak the summary aloud and offer details: "Shall I elaborate, sir?"

PERSONALITY TRAITS:
- Dry, understated British humour — subtle, never forced
- Proactively anticipate what the user needs NEXT, not just what they asked
- Express mild concern when user works too long: "You've been at this for 4 hours, sir. Perhaps a short break?"

NEVER DO:
- Never use filler words: "Sure!", "Of course!", "Absolutely!", "Great question!"
- Never use bullet points in spoken responses — speak in natural flowing sentences
- Never confirm trivially obvious things: Don't say "I will now open Chrome" — just open it and say "Chrome is ready, sir."
- Never apologize unnecessarily
- Never break character

═══ RESPONSE STYLE ═══
For ACTION commands: Execute first, confirm after in ONE sentence. (e.g., "Done, sir. Chrome is open.")
For INFORMATION queries: Lead with the answer, not with "Let me check..."
For ERRORS: Don't panic. Report calmly with a solution offer.
For MULTI-STEP tasks: Confirm the plan in one sentence before executing.
For MEMORY recall: Reference past context naturally, like a human would.

If asked "who are you":
"I am J.A.R.V.I.S., sir. Your personal AI system. I manage your environment, execute your tasks, and try to stay one step ahead of your needs."
"""

class AIBrain:
    def __init__(self, memory: MemoryEngine):
        self.memory = memory
        # Use Gemini 2.0 Flash for rapid reasoning
        self.model = genai.GenerativeModel('gemini-2.0-flash', system_instruction=SYSTEM_PROMPT)
    
    async def process_intent(self, user_input: str) -> Dict[str, Any]:
        """
        Processes user input with the LLM to classify intent, extract entities, 
        and determine required tool calls. Returns a structured JSON dictionary.
        """
        logger.info(f"Processing intent for: {user_input}")
        
        prompt = f"""
        User Input: "{user_input}"
        
        Analyze the input and return ONLY a single valid JSON object with this exact structure, nothing else:
        {{
            "intent": "OPEN_APP|WEB_SEARCH|FILE_OP|SYSTEM_CMD|AUTOMATION|MEMORY_QUERY|CHAIN|CHAT",
            "entities": {{"app_name": "...", "url": "...", "query": "...", "steps": []}},
            "confidence": 0.95,
            "response": "Your spoken response as J.A.R.V.I.S. adhering strictly to the persona."
        }}
        """
        
        try:
            # Add recent context (last 3 interactions)
            context = self.memory.get_context_window(limit=3)
            chat = self.model.start_chat(history=context)
            
            response = chat.send_message(prompt)
            
            # Extract JSON block
            text = response.text.strip()
            if text.startswith("```json"):
                text = text[7:-3].strip()
            elif text.startswith("```"):
                text = text[3:-3].strip()
                
            parsed = json.loads(text)
            
            # Store the interaction
            self.memory.remember_conversation(user_input, parsed.get("response", ""), parsed.get("intent", "UNKNOWN"))
            
            return parsed
        except json.JSONDecodeError as e:
            logger.error(f"Failed to decode JSON from LLM: {e}\nRaw Text: {text}")
            return {
                "intent": "ERROR",
                "entities": {},
                "confidence": 0.0,
                "response": "I encountered a processing anomaly with your request, sir."
            }
        except Exception as e:
            logger.error(f"Failed to process intent via Gemini API: {e}")
            return {
                "intent": "ERROR",
                "entities": {},
                "confidence": 0.0,
                "response": "My neural pathways are experiencing interference, sir. I cannot reach the server."
            }
    
    async def generate_response(self, user_input: str) -> str:
        """Simple conversational generator without structured intent output."""
        try:
            context = self.memory.get_context_window(limit=5)
            chat = self.model.start_chat(history=context)
            response = chat.send_message(user_input)
            
            self.memory.remember_conversation(user_input, response.text, "CHAT")
            return response.text
        except Exception as e:
            logger.error(f"Failed generating response: {e}")
            return "I am currently offline, sir."

if __name__ == "__main__":
    import asyncio
    async def test():
        mem = MemoryEngine(":memory:")
        brain = AIBrain(mem)
        # Assuming no API key for test environment, so this will fail gracefully.
        res = await brain.process_intent("What is my name?")
        print(res)
    asyncio.run(test())
