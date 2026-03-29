"""
main.py
The JARVIS Asynchronous Entry Point.
"""

import asyncio
import os
from dotenv import load_dotenv

from logger import get_logger
from memory_engine import MemoryEngine
from ai_brain import AIBrain
from command_parser import CommandParser
from voice_engine import VoiceEngine
from task_engine import TaskEngine

load_dotenv()
logger = get_logger()

class JarvisApp:
    def __init__(self):
        logger.info("Initializing J.A.R.V.I.S. Core Systems...")
        self.memory = MemoryEngine()
        self.brain = AIBrain(self.memory)
        self.parser = CommandParser()
        self.voice = VoiceEngine()
        self.tasks = TaskEngine(self.memory)
        self.user_name = os.getenv("USER_NAME", "Sir")
        
    async def boot_sequence(self):
        """Startup routine."""
        logger.info("Boot sequence initiated.")
        greeting = f"Systems online. Good evening, {self.user_name}."
        
        print("\n" + "="*50)
        print(f"[{greeting}]")
        print("="*50 + "\n")
        
        await self.voice.speak(greeting)

    async def process_user_input(self, text_input: str):
        """The main loop processing pipeline."""
        if not text_input.strip():
            return
            
        print(f"\n[User]: {text_input}")
        
        # 1. Brain extracts intent and generates persona-based response
        llm_payload = await self.brain.process_intent(text_input)
        
        # 2. Parse into actionable Task objects
        task_list = self.parser.parse_llm_output(llm_payload)
        
        # 3. Output JARVIS' response
        response_text = llm_payload.get("response", "Understood, sir.")
        print(f"[JARVIS]: {response_text}")
        
        speak_task = asyncio.create_task(self.voice.speak(response_text))
        
        # 4. Execute the tasks
        if task_list:
            await self.tasks.execute_chain(task_list)
            
        await speak_task

    async def run_interactive_loop(self):
        """Runs the CLI input loop."""
        await self.boot_sequence()
        while True:
            try:
                user_msg = await asyncio.to_thread(input, "\nCommand > ")
                if user_msg.lower() in ["exit", "quit", "shutdown"]:
                    await self.voice.speak("Powering down systems. Goodbye, sir.")
                    break
                await self.process_user_input(user_msg)
            except KeyboardInterrupt:
                logger.info("Manual termination received.")
                break
            except Exception as e:
                logger.error(f"Main loop error: {e}")

if __name__ == "__main__":
    app = JarvisApp()
    asyncio.run(app.run_interactive_loop())
