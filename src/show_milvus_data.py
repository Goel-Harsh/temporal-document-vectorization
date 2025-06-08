import time
from pymilvus import (
    connections, FieldSchema, CollectionSchema, DataType, Collection, utility
)

MILVUS_HOST = "localhost"
MILVUS_PORT = "19530"
COLLECTION_NAME = "documents"

connections.connect(host=MILVUS_HOST, port=MILVUS_PORT)

# Define schema if collection does not exist
if not utility.has_collection(COLLECTION_NAME):
    fields = [
        FieldSchema(name="file_id", dtype=DataType.VARCHAR, max_length=64, is_primary=True, auto_id=False),
        FieldSchema(name="chunk_index", dtype=DataType.INT64),
        FieldSchema(name="text", dtype=DataType.VARCHAR, max_length=2048),
        FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=1536),  # Set dim to your embedding size
    ]
    schema = CollectionSchema(fields, description="Document chunks and embeddings")
    collection = Collection(COLLECTION_NAME, schema)
    print(f"Created collection '{COLLECTION_NAME}'")

    # Create index on the embedding field
    index_params = {
        "index_type": "IVF_FLAT",
        "metric_type": "L2",
        "params": {"nlist": 128}
    }
    collection.create_index(field_name="embedding", index_params=index_params)
    print("Created index on 'embedding' field.")

    # Wait for index to be built
    while not collection.has_index():
        print("Waiting for index to be built...")
        time.sleep(1)
else:
    collection = Collection(COLLECTION_NAME)
    print(f"Loaded collection '{COLLECTION_NAME}'")

collection.load()

# Retrieve all data (limit for demo; adjust as needed)
results = collection.query(expr="", output_fields=["file_id", "chunk_index", "text", "embedding"], limit=10)

for record in results:
    print("File ID:", record["file_id"])
    print("Chunk Index:", record["chunk_index"])
    print("Text:", record["text"])
    print("Embedding (first 5 dims):", record["embedding"][:5], "...")
    print("-" * 40)
