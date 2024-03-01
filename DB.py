from langchain_community.document_loaders import JSONLoader
from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import HuggingFaceDatasetLoader


def connect_db(
    dataset_name="openai_humaneval", page_content_column="canonical_solution"
):
    embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    loader = HuggingFaceDatasetLoader(dataset_name, page_content_column)
    data = loader.load()
    db = Chroma.from_documents(data, embedding_function)
    return db


def get_few_shots(db, code):
    query = code
    docs = db.similarity_search(query)
    # print("def" + docs[0].metadata['test'].split("def", maxsplit = 1)[1])
    # print(docs[3].metadata)
    test_cases_of_few_shot = docs[3].metadata["test"]
    return test_cases_of_few_shot
