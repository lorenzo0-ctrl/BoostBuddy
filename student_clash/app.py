import sys
from pathlib import Path

# Aggiungi src al PYTHONPATH
sys.path.append(str(Path(__file__).parent / "src"))

import chainlit as cl
from student_clash.crew import create_crew

@cl.on_chat_start
async def start():
    await cl.Message("Ciao! Inviami un messaggio e lo passo al CrewAI.").send()

@cl.on_message
async def main(message: cl.Message):
    user_input = message.content
    crew = create_crew()
    result = crew.run(user_input)
    await cl.Message(result).send()