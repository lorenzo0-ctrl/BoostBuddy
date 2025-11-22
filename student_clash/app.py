import chainlit as cl
from student_clash.crew import BalancedLifeCrew

@cl.on_chat_start
async def start():
    """Welcome message when user opens the chat"""
    await cl.Message(
        content="👋 Hi! I'm your assistant for a balanced life. "
                "I can help you with fitness, nutrition and stress management. "
                "How can I help you today?"
    ).send()

@cl.on_message
async def main(message: cl.Message):
    """Handles every user message"""
    
    processing_msg = cl.Message(content="🤖 I'm analyzing your request...")
    await processing_msg.send()
    
    try:
        # Crea l'istanza della crew e ottieni la crew
        balanced_life_crew = BalancedLifeCrew()
        crew = balanced_life_crew.crew()
        
        # Esegue la crew
        result = crew.kickoff(inputs={
            "user_request": message.content
        })
        
        final_response = result.raw if hasattr(result, 'raw') else str(result)
        
        await cl.Message(content=final_response).send()
        
    except Exception as e:
        await cl.Message(
            content=f"An error occurred: {str(e)}"
        ).send()