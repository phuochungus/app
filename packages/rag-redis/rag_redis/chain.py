from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.prompts import ChatPromptTemplate
from langchain.pydantic_v1 import BaseModel
from langchain.schema.output_parser import StrOutputParser
from langchain.schema.runnable import RunnableParallel, RunnablePassthrough
from langchain.vectorstores import Redis

from rag_redis.config import (
    INDEX_NAME,
    INDEX_SCHEMA,
    REDIS_URL,
)


# Make this look better in the docs.
class Question(BaseModel):
    __root__: str


# Init Embeddings
embedder = OpenAIEmbeddings()

# Connect to pre-loaded vectorstore
# run the ingest.py script to populate this
vectorstore = Redis.from_existing_index(
    embedding=embedder, index_name=INDEX_NAME, schema=INDEX_SCHEMA, redis_url=REDIS_URL
)
retriever = vectorstore.as_retriever(search_type="mmr")


# Define our prompt
template = """
Use the following pieces of context from ApartmentManagementDocument and
ProjectManagementDocument to answer the question. Do not make up an answer 
if there is no context provided to help answer it. Answer the question in
the same language as the question is asked.

Context:
---------
{context}

---------
Question: {question}
---------

Answer:
"""


prompt = ChatPromptTemplate.from_template(template)

# Cache
from langchain.cache import InMemoryCache
from langchain.globals import set_llm_cache
set_llm_cache(InMemoryCache())

# RAG Chain
model = ChatOpenAI(model_name="gpt-3.5-turbo")
chain = (
    RunnableParallel({"context": retriever, "question": RunnablePassthrough()})
    | prompt
    | model
    | StrOutputParser()
).with_types(input_type=Question)
