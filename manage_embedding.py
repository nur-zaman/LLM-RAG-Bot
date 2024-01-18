from llama_index import SimpleDirectoryReader,VectorStoreIndex  , load_index_from_storage
from llama_index.storage.storage_context import StorageContext
from dotenv import load_dotenv
import logging
import sys


load_dotenv()

# enable INFO level logging
logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))


async def load_index(directory_path : str = r'data'):
    documents = SimpleDirectoryReader(directory_path, filename_as_id=True).load_data()
    print(f"loaded documents with {len(documents)} pages")
    try:
        # Rebuild storage context
        storage_context = StorageContext.from_defaults(persist_dir="./storage")
        # Try to load the index from storage
        index = load_index_from_storage(storage_context)
        logging.info("Index loaded from storage.")
    except FileNotFoundError:

        logging.info("Index not found. Creating a new one...")
        index = VectorStoreIndex.from_documents(documents)
        # Persist index to disk
        index.storage_context.persist()
        logging.info("New index created and persisted to storage.")

    return index

async def update_index(directory_path : str = r'data'):
    try:
        documents = SimpleDirectoryReader(directory_path, filename_as_id=True).load_data()
    except FileNotFoundError:
        logging.error("Invalid document directory path.")
        return None
    try:
        # Rebuild storage context
        storage_context = StorageContext.from_defaults(persist_dir="./storage")
        # Try to load the index from storage
        index = load_index_from_storage(storage_context)
        logging.info("Existing index loaded from storage.")
        refreshed_docs = index.refresh_ref_docs(documents, update_kwargs={"delete_kwargs": {"delete_from_docstore": True}})
        # index.update_ref_doc()
        print(refreshed_docs)
        print('Number of newly inserted/refreshed docs: ', sum(refreshed_docs))

        index.storage_context.persist()
        logging.info("Index refreshed and persisted to storage.")
        return refreshed_docs

        
    except FileNotFoundError:
    # Run refresh_ref_docs function to check for document updates
        logging.error("Index is not created yet.")
        return None

