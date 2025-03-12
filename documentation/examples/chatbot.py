import os, sys
import logging
from typing import Any, Dict, List
import chromadb
from chromadb.errors import InvalidCollectionException
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import Settings
from llama_index.core import StorageContext
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.core import StorageContext
from llama_index.llms.azure_openai import AzureOpenAI
from llama_index.embeddings.azure_openai import AzureOpenAIEmbedding
from monocle_apptrace.instrumentation.common.instrumentor import setup_monocle_telemetry
setup_monocle_telemetry(workflow_name = "my-chatbot")
chroma_collection_name="monocle_demo"

# Create vectore store and load data
def setup_embedding(chroma_vector_store: ChromaVectorStore, embed_model):
    documents = SimpleDirectoryReader(input_files= ["coffee.txt"]).load_data()

    storage_context = StorageContext.from_defaults(vector_store=chroma_vector_store)
    index = VectorStoreIndex.from_documents(
        documents, storage_context=storage_context, embed_model=embed_model
    )
    index.storage_context.persist(persist_dir="vector_store")

def get_vector_index() -> VectorStoreIndex:
    chroma_client = chromadb.PersistentClient(path="vector_store")
    create_embedding = False
    embed_model = AzureOpenAIEmbedding(
        model_name="text-embedding-3-large",
        azure_deployment=os.environ.get("AZURE_OPENAI_EMBED_API_DEPLOYMENT"),
        api_key=os.environ.get("AZURE_OPENAI_API_KEY"),
        api_version=os.environ.get("AZURE_OPENAI_API_VERSION"),
        azure_endpoint=os.environ.get("AZURE_OPENAI_ENDPOINT")
    )
    try:
        chroma_collection = chroma_client.get_collection(chroma_collection_name)
    except InvalidCollectionException:
        chroma_collection = chroma_client.create_collection(chroma_collection_name)
        create_embedding = True
    # construct vector store
    chroma_vector_store = ChromaVectorStore(
        chroma_collection=chroma_collection,
    )
    if create_embedding == True:
        setup_embedding(chroma_vector_store, embed_model)
    return VectorStoreIndex.from_vector_store(vector_store=chroma_vector_store, embed_model=embed_model)

def run(index: VectorStoreIndex):
    az_llm = AzureOpenAI(deployment_id=os.environ.get("AZURE_OPENAI_API_DEPLOYMENT"),
                     api_key=os.environ.get("AZURE_OPENAI_API_KEY"), 
                     api_version=os.environ.get("AZURE_OPENAI_API_VERSION"), 
                     azure_endpoint=os.environ.get("AZURE_OPENAI_ENDPOINT"))

    query_engine = index.as_query_engine(llm=az_llm)

    while True:
        prompt = input("\nAsk a coffee question [Press return to exit]: ")
        if prompt == "":
            break
        response = query_engine.query(prompt)
        print(response)

def main():
    logger = logging.getLogger()
    logger.setLevel(logging.ERROR)
    index = get_vector_index()
    run(index)

if __name__ == "__main__":
    main()

