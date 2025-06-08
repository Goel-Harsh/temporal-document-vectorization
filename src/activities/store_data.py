from pymilvus import Collection, connections, utility
from temporalio import activity

@activity.defn
async def store_data(file_id: str, chunk_index: int, original_text: str, embedding_vector: list, collection_name: str):
    try:
        connections.connect("default", host='localhost', port='19530')

        if not utility.has_collection(collection_name):
            raise Exception(f"Collection {collection_name} does not exist.")

        collection = Collection(collection_name)
        # embedding_vector must be a flat list of floats
        if not isinstance(embedding_vector, list) or not all(isinstance(x, float) for x in embedding_vector):
            raise Exception("embedding_vector must be a flat list of floats")

        data = [
            [file_id],
            [chunk_index],
            [original_text],
            [embedding_vector]
        ]
        insert_result = collection.insert(data)
        print(f"Inserted {insert_result.insert_count} records into collection '{collection_name}'.")
        if insert_result.insert_count == 0:
            raise Exception("Failed to insert data into Milvus.")
        
        return f"Inserted {insert_result.insert_count} records into collection '{collection_name}'."
    except Exception as e:
        print(f"Error in store_data activity: {e}")
        raise
    finally:
        connections.disconnect("default")
