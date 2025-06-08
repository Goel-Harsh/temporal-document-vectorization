import asyncio
from temporalio.client import Client
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
async def main():
    client = await Client.connect("localhost:7233")
    file_id = input("Enter file ID: ")
    file_url = input("Enter file URL: ")
    filetype = input("Enter file type (e.g., pdf, docx): ")
    result = await client.start_workflow(
        workflow="DocumentWorkflow",
        args=[file_id, file_url, filetype],
        id=f"doc-workflow-{file_id}",
        task_queue="document_processing",
    )
    logger.info("Workflow started: %s", result)

if __name__ == "__main__":
    asyncio.run(main())
