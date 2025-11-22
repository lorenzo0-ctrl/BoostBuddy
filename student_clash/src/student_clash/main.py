#!/usr/bin/env python
import sys
import warnings
import json
from datetime import datetime
from dotenv import load_dotenv
import os
from openai import OpenAI
from my_project.crew import BalancedLifeCrew
from my_project.memory import MemoryManager  # il file memory.py con MemoryManager

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
REQUIRED_FIELDS = ["fitness_level", "diet_pref", "stress_level", "time_available"]
## prova

def extract_inputs(user_message: str):
    prompt = f"""
    Extract the following information from the user's message in JSON format:
    - fitness_level (beginner/intermediate/advanced)
    - diet_pref (any dietary preference)
    - stress_level (low/medium/high)
    - time_available (minutes)
    
    If any field is missing, leave it as null.

    User message: "{user_message}"
    Return only JSON.
    """
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    try:
        data = json.loads(response.choices[0].message["content"])
        return data
    except json.JSONDecodeError:
        return None


def main():
    user_message = input("You: ")

    # Prova a estrarre JSON dai task
    extracted = extract_inputs(user_message)
    memory = MemoryManager()

    if extracted and all(field in extracted and extracted[field] is not None for field in REQUIRED_FIELDS):
        # Aggiorno la memoria con i dati estratti
        for field in REQUIRED_FIELDS:
            memory.update(field, extracted[field])

        # Eseguo la crew
        try:
            crew_instance = BalancedLifeCrew()
            plan = crew_instance.crew().kickoff(inputs=memory.memory)  # passo la memoria aggiornata
            print("\n💡 Generated Daily Plan:\n")
            for task_name, output in plan.items():
                print(f"{task_name}: {output}\n")
            
            # Aggiorno memoria con output dei task se necessario
            if 'fitness_task' in plan:
                memory.update("last_workout", plan['fitness_task'])
            if 'diet_task' in plan:
                memory.update("last_meal_plan", plan['diet_task'])

        except Exception as e:
            print(f"An error occurred while running the crew: {e}")
    else:
        print("I'm unable to do this task.")

if __name__ == "__main__":
    main()
