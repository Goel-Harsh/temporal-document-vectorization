from unstructured.partition.auto import partition
from temporalio import activity
import io

@activity.defn
async def parse_document(document_content: bytes, filetype: str) -> list:
    try:
        file_obj = io.BytesIO(document_content)
        chunks = partition(file=file_obj, filetype=filetype)
        return [chunk.text for chunk in chunks]
    except Exception as e:
        raise RuntimeError(f"Error parsing document: {str(e)}")
