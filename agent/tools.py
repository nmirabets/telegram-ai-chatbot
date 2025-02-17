import os
import uuid
from dotenv import load_dotenv
from pinecone import Pinecone
from openai import OpenAI
from datetime import datetime, timezone


load_dotenv()

# Initialize Pinecone for vector database
pc = Pinecone(os.getenv("PINECONE_API_KEY"))
# Initialize the vector database index
index = pc.Index(os.getenv("PINECONE_INDEX_NAME"))
# Initialize OpenAI for embeddings 
client = OpenAI()

# Define the tools
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "save_memory",
            "description": "Save a memory to the vector database",
            "parameters": {
                "type": "object",
                "properties": {
                    "memory": {"type": "string"}
                },
                "required": ["memory"]
            },
        },
    },
]

# Function to get the embeddings of a string
def get_embeddings(string_to_embed):
    response = client.embeddings.create(
        input=string_to_embed,
        model="text-embedding-ada-002"
    )
    return response.data[0].embedding

def save_memory(memory):
    # Step 1: Embed the memory
    vector = get_embeddings(memory)
    # Step 2: Build the vector document to be stored
    user_id = "1234"
    path = "user/{user_id}/recall/{event_id}"
    current_time = datetime.now(tz=timezone.utc)
    path = path.format(
        user_id=user_id,
        event_id=str(uuid.uuid4()),
    )
    documents = [
        {
            "id": str(uuid.uuid4()),
            "values": vector,
            "metadata": {
                "payload": memory,
                "path": path,
                "timestamp": str(current_time),
                "type": "recall", # Define the type of document i.e recall memory
                "user_id": user_id,
            },
        }
    ]
    # Step 3: Store the vector document in the vector database
    index.upsert(
        vectors=documents,
        namespace=os.getenv("PINECONE_NAMESPACE")
    )
    return "Memory saved successfully"

def load_memories(prompt):
    user_id = "1234"
    top_k = 3
    vector = get_embeddings(prompt)
    response = index.query(
        vector=vector,
        filter={
            "user_id": {"$eq": user_id},
            "type": {"$eq": "recall"},
        },
        namespace=os.getenv("PINECONE_NAMESPACE"),
        include_metadata=True,
        top_k=top_k,
    )
    memories = []
    if matches := response.get("matches"):
        memories = [m["metadata"]["payload"] for m in matches]
        memories
    return memories