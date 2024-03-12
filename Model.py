from langchain_community.llms import HuggingFaceHub
from langchain_community.chat_models.huggingface import ChatHuggingFace
import openai


def InitializeModel(
    htoken, model_id="mistralai/Mixtral-8x7B-Instruct-v0.1", max_new_tokens=20000
):
    # model_id='databricks/dolly-v2-3b'
    llm = HuggingFaceHub(
        repo_id=model_id,
        huggingfacehub_api_token=htoken,
        task="text-generation",
        model_kwargs={
            "temperature": 0.1,  # can't be 0
            "max_new_tokens": max_new_tokens,
        },
        cache=False,
    )
    chat_model = ChatHuggingFace(llm=llm)
    return llm, chat_model


def InitializeGptModel(token, model_id="gpt-3.5-turbo", max_new_tokens=20000):
    # model_id='databricks/dolly-v2-3b'
    openai.api_key = token
    llm = model_id

    return llm, llm


def InitializeModelArbiter(
    htoken, repo_id="google/gemma-7b-it", max_new_tokens=5000
):
    llm = HuggingFaceHub(
        repo_id=repo_id,
        huggingfacehub_api_token=htoken,
        task="text-generation",
        model_kwargs={
            "temperature": 0.1,  # can't be 0
            "max_new_tokens": max_new_tokens,
        },
        cache=False,
    )
    chat_model = ChatHuggingFace(llm=llm)
    return llm, chat_model