from langchain.vectorstores.cassandra import Cassandra
from langchain.indexes.vectorstore import VectorStoreIndexWrapper
from langchain.llms import OpenAI
from langchain.embeddings import OpenAIEmbeddings

from typing_extensions import Concatenate
# Support for dataset retrieval with Hugging Face
from datasets import load_dataset

# With CassIO, the engine powering the Astra DB integration in LangChain,
# you will also initialize the DB connection:
import cassio
from PyPDF2 import PdfReader


ASTRA_DB_APPLICATION_TOKEN = "AstraCS:fJuQoRdDFkzATkUoJYmKfPQG:f066cf426b30d6862c9d3d63e9b637424177283e467c4c2ccec718b9dc411626" # enter the "AstraCS:..." string found in in your Token JSON file
ASTRA_DB_ID = "d9a42da8-b36b-4c34-8e56-ad93eef80a64" # enter your Database ID

OPENAI_API_KEY = "" # enter your OpenAI key

# provide the path of  pdf file/files.
pdfreader = PdfReader('saudi_law.pdf')

# read text from pdf
raw_text = ''
for i, page in enumerate(pdfreader.pages):
    content = page.extract_text()
    if content:
        raw_text += content
        
print(raw_text)


#Initialize the connection to your database:
cassio.init(token=ASTRA_DB_APPLICATION_TOKEN, database_id=ASTRA_DB_ID)

#Create the LangChain embedding and LLM objects for later usage:
llm = OpenAI(openai_api_key=OPENAI_API_KEY)
embedding = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)

#Create your LangChain vector store ... backed by Astra DB!
astra_vector_store = Cassandra(
    embedding=embedding,
    table_name="law_saudi_demo",
    session=None,
    keyspace=None,
)



from langchain.text_splitter import CharacterTextSplitter
# We need to split the text using Character Text Split such that it sshould not increse token size
text_splitter = CharacterTextSplitter(
    separator = "\n",
    chunk_size = 1000,
    chunk_overlap  = 100,
    length_function = len,
)
texts = text_splitter.split_text(raw_text)
print(texts)



astra_vector_store.add_texts(texts[:50])

print("Inserted %i headlines." % len(texts[:50]))

astra_vector_index = VectorStoreIndexWrapper(vectorstore=astra_vector_store)



first_question = True
while True:
    if first_question:
        query_text = input("\nEnter your question (or type 'quit' to exit): ").strip()
    else:
        query_text = input("\nWhat's your next question (or type 'quit' to exit): ").strip()

    if query_text.lower() == "quit":
        break

    if query_text == "":
        continue

    first_question = False

    print("\nQUESTION: \"%s\"" % query_text)
    answer = astra_vector_index.query(query_text, llm=llm).strip()
    print("ANSWER: \"%s\"\n" % answer)

    print("FIRST DOCUMENTS BY RELEVANCE:")
    for doc, score in astra_vector_store.similarity_search_with_score(query_text, k=4):
        print("    [%0.4f] \"%s ...\"" % (score, doc.page_content[:135]))