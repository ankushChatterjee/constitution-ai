from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Pinecone
from langchain.document_loaders import PyPDFLoader
import pinecone
import os

consitution_file="./constitution.pdf"
pinecone_api_key=os.environ['PINECONE_API_KEY']
pinecone_env="us-east4-gcp"
index_name="constitutionai"
openai_key=os.environ['OPENAI_API_KEY']

pinecone.init(
    api_key=pinecone_api_key,  # find at app.pinecone.io
    environment=pinecone_env  
)

embeddings = OpenAIEmbeddings(openai_api_key=openai_key)

loader = PyPDFLoader(consitution_file)
pages = loader.load_and_split()

search = Pinecone.from_documents(pages, embeddings, index_name=index_name)

query = "What is the role of the parliament?"
docs = search.similarity_search(query)

print(docs[0].page_content)
