from langchain_community.llms import HuggingFaceHub
from langchain_community.chat_models.huggingface import ChatHuggingFace


def InitializeModel(htoken):
    model_id = "mistralai/Mixtral-8x7B-Instruct-v0.1"
    # model_id='databricks/dolly-v2-3b'
    llm = HuggingFaceHub(
        repo_id=model_id,
        model_kwargs={
            "temperature": 0.1,  # can't be 0
            "max_new_tokens": 20000,
        },
        huggingfacehub_api_token=htoken,
        task="text-generation",
        cache=False,
    )
    chat_model = ChatHuggingFace(llm=llm)
    return llm, chat_model
