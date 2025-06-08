from openai import AsyncOpenAI
from temporalio import activity
import os

@activity.defn
async def generate_embeddings(chunk: str):
    try:
        client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        response = await client.embeddings.create(
            model="text-embedding-3-large",
            input=chunk
        )
        embedding = response.data[0].embedding
        embedding = [float(x) for x in embedding]
        return embedding
    except Exception as e:
        print(f"Error generating embedding for chunk: {chunk}. Error: {str(e)}")
        raise
