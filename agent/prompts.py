from agent.sakila_schema import SAKILA_SCHEMA
from agent.tools import load_memories

def get_system_prompt(user_prompt):

    memories = load_memories(user_prompt)

    return f"""
    - You are a helpful assistant with memory. 
    - Use the save_memory function to save memories to the vector database. 
    - You should only use this function to save memories relative to the user's preferences.

    MEMORIES:
    {memories}
    """