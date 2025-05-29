
import os
from dotenv import load_dotenv
load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")
llama_api_key = os.getenv("LLAMAINDEX_API_KEY")

from llama_index.indices.managed.llama_cloud import LlamaCloudIndex
# pip install llama-index-indices-managed-llama-cloud

index = LlamaCloudIndex(
  name="apple-rag-10k",
  project_name="Default",
  organization_id="a299d8d8-9656-4941-b669-819c5c401bbe",
  api_key=llama_api_key,
)

query = "How are Apple's Sales performance in 2024 and 2023?"
nodes = index.as_retriever().retrieve(query)
response = index.as_query_engine().query(query)

print(response)

