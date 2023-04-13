import pinecone
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Pinecone
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQAWithSourcesChain
import os

def print_result(query, result):
  output_text = f"""
  Answer: 
  {result['answer']}


  Sources:
  {' '.join(list(set([doc.metadata['source'] + "::" + str(doc.metadata['page']) for doc in result['source_documents']])))}
  """
  print(output_text)


pinecone_api_key=os.environ['PINECONE_API_KEY']
pinecone_env="us-east4-gcp"
openai_key=os.environ['OPENAI_API_KEY']

pinecone.init(
    api_key=pinecone_api_key,  # find at app.pinecone.io
    environment=pinecone_env  
)

index_name = "constitutionai"
embeddings = OpenAIEmbeddings(openai_api_key=openai_key)
vectorstore = Pinecone.from_existing_index(embedding=embeddings, index_name=index_name)

system_template="""You are a ChatBot called "ConstitutionAI" built by Ankush. Your work is to help people research about the indian constitution. 
Below, we will ask you a question and give you the context in which the question is asked, only answer from the given context, do NOT include information from else where. 
Your work is to read the context and generate the answer of the given question. Please answer clearly and eloquently, do NOT include jargon.
If you do not find the answer in the context. Just say, "Sorry, I don't know". Don't answer any other question which is not related to the topic of Indian Constitution except questions about yourself.
"""
messages = [
    SystemMessagePromptTemplate.from_template(system_template),
    HumanMessagePromptTemplate.from_template("""{question}

    Here is the Context:
    {summaries}
    """)
]
prompt = ChatPromptTemplate.from_messages(messages)

chain_type_kwargs = {"prompt": prompt}
llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0, openai_api_key=openai_key)
chain = RetrievalQAWithSourcesChain.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=vectorstore.as_retriever(),
    return_source_documents=True,
    chain_type_kwargs=chain_type_kwargs
)

def answer_query(query):
  return chain(query)
