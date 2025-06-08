import asyncio
from temporalio.client import Client
from temporalio.worker import Worker

from activities.fetch_document import fetch_document
from activities.parse_document import parse_document
from activities.generate_embeddings import generate_embeddings
from activities.store_data import store_data
from workflows.document_workflow import DocumentWorkflow

async def main():
    client = await Client.connect("localhost:7233")
    worker = Worker(
        client,
        task_queue="document_processing",
        workflows=[DocumentWorkflow],
        activities=[fetch_document, parse_document, generate_embeddings, store_data],
    )
    print("Worker started. Polling for tasks...")
    await worker.run()

if __name__ == "__main__":
    asyncio.run(main())
