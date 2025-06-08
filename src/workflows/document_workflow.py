from temporalio import workflow
import os
import logging
import asyncio
from datetime import timedelta

logger = logging.getLogger(__name__)

SUPPORTED_TYPES = {'.docx', '.doc', '.xlsx', '.xls'}
COLLECTION_NAME = "documents"

@workflow.defn
class DocumentWorkflow:
    @workflow.run
    async def run(self, file_id: str, file_url: str, filetype: str):
        # Step 1: Fetch Document
        document_content = await workflow.execute_activity(
            "fetch_document", args=[file_url, filetype], start_to_close_timeout=timedelta(seconds=30)
        )
        # Step 2: Parse Document
        chunks = await workflow.execute_activity(
            "parse_document", args=[document_content, filetype], start_to_close_timeout=timedelta(seconds=30)
        )
        logger.info(f"Parsed document into {len(chunks)} chunks for file ID: {file_id}")

        # Step 3: Generate Embeddings
        embedding_tasks = [
            workflow.execute_activity(
                "generate_embeddings", args=[chunk], start_to_close_timeout=timedelta(seconds=30)
            ) for chunk in chunks
        ]
        embeddings = await asyncio.gather(*embedding_tasks)
        logger.info(f"Generated embeddings for {len(embeddings)} chunks for file ID: {file_id}")
        # Step 4: Store Data

        store_tasks = []
        for idx, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
            if embedding is None:
                print(f"Embedding generation failed for chunk {idx}. Skipping.")
                continue
            print(f"embedding type: {type(embedding)}, first 5: {embedding[:5]}")
            store_tasks.append(
                workflow.execute_activity(
                    "store_data",
                    args=[file_id, idx, chunk, embedding, COLLECTION_NAME],
                    start_to_close_timeout=timedelta(seconds=300)
                )
            )
        await asyncio.gather(*store_tasks)
        logger.info(f"Stored data for file ID: {file_id}")

        # Workflow Completion
        return "Document processing completed successfully."
