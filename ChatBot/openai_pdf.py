from PyPDF2 import PdfReader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
import os
import json
os.environ["OPENAI_API_KEY"] = ""

def extract_text_from_pdf(pdf_path):
    text = ""
    pdf_reader = PdfReader(pdf_path)
    for i, page in enumerate(pdf_reader.pages):
        content = page.extract_text()
        if content:
            text += content
    return text

def ask_questions(questions):
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

    questions = f'{questions} '
    docs = document_search.similarity_search(questions)
    answer = chain.run(input_documents=docs, question=questions)
    print(f"Answer: {answer}")

    # Ask user if they want to save the answer
    save_answer = input("Do you want to save the answer? (yes/no): ").lower()

    if save_answer == "yes":
        # Update intents.json file
        intents_file_path = 'intents.json'
        with open(intents_file_path, 'r', encoding='utf-8') as intents_file:
            intents_data = json.load(intents_file)

      # Add new pattern, response, and tag
        new_pattern = questions
        new_response = answer
        new_tag = questions.split()[0]  # Use the first word as the tag

        intents_data['intents'].append({
            'tag': f"{new_tag}",
            'patterns': f"{new_pattern}",
            'responses': f"{new_response}"
        })
        
        print(new_pattern)
        print(new_response)
        print(new_tag)

        # Save updated data back to intents.json
        with open(intents_file_path, 'w', encoding='utf-8') as intents_file:
            json.dump(intents_data, intents_file, ensure_ascii=False, indent=4)

        print("Answer saved to intents.json.")
    else:
        print("Answer not saved.")
