from PyPDF2 import PdfReader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
import os

os.environ["OPENAI_API_KEY"] = ""

def extract_text_from_pdf(pdf_path):
    text = ""
    pdf_reader = PdfReader(pdf_path)
    for i, page in enumerate(pdf_reader.pages):
        content = page.extract_text()
        if content:
            text += content
    return text

def ask_questions():
    pdf_path = 'arabic_law.pdf'
    raw_text = extract_text_from_pdf(pdf_path)

    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=800,
        chunk_overlap=200,
        length_function=len,
    )

    texts = text_splitter.split_text(raw_text)

    # Download embeddings from OpenAI
    embeddings = OpenAIEmbeddings()

    document_search = FAISS.from_texts(texts, embeddings)

    chain = load_qa_chain(OpenAI(), chain_type="stuff")

    while True:
        query = input("Ask a question (type 'quit' to exit): ")
        if query.lower() == 'quit':
            break
        else:
            docs = document_search.similarity_search(query)
            answer = chain.run(input_documents=docs, question=query)
            print("Answer:", answer)
            print()

if __name__ == "__main__":
    ask_questions()
