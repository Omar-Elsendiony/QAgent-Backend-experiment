from langchain_community.document_loaders import JSONLoader
from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import HuggingFaceDatasetLoader

from Utilities import get_function_name
import re


def connect_db(
    dataset_name="openai_humaneval", page_content_column="canonical_solution"
):
    embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    loader = HuggingFaceDatasetLoader(dataset_name, page_content_column)
    data = loader.load()
    db = Chroma.from_documents(data, embedding_function)
    return db


def get_one_shot(db, code):
    query = code
    docs = db.similarity_search(query)
    test_cases_of_few_shot = docs[0].metadata["test"]
    description_of_few_shot = docs[0].metadata["prompt"]

    return test_cases_of_few_shot


def get_few_shots(db, code):
    test_cases_of_few_shotList = []
    description_of_few_shotList = []
    code_of_few_shotList = []
    query = code
    docs = db.similarity_search(query)
    for i in range(1, 4):

        test_cases_of_few_shot = docs[i].metadata["test"]
        description_of_few_shot = docs[i].metadata["prompt"]
        code_of_few_shot = docs[i].page_content
        # get the function header
        description_of_few_shot = get_function_name(description_of_few_shot)
        code_of_few_shot = re.sub(r"\\n", "\n", code_of_few_shot)
        # print(test_cases_of_few_shot)
        code_of_few_shot = description_of_few_shot + code_of_few_shot
        test_cases_of_few_shotList.append(test_cases_of_few_shot)
        description_of_few_shotList.append(description_of_few_shot)
        code_of_few_shotList.append(code_of_few_shot)
    return (code_of_few_shotList, test_cases_of_few_shotList)
