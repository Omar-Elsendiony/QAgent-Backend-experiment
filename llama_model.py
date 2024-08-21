import os
from typing import List, Optional

from llama_index.llms.huggingface import HuggingFaceLLM
from llama_index.llms.huggingface_api import HuggingFaceInferenceAPI

# URL = "mistralai/Mixtral-8x7B-Instruct-v0.1"
# remotely_run = HuggingFaceInferenceAPI(
#     model_name="HuggingFaceH4/zephyr-7b-alpha", token=os.getenv("HUGGINGFACEHUB_API_TOKEN")
# )

# completion_response = remotely_run.complete("To infinity, and")
# print(completion_response)

class LlamaModel:
    def __init__(self, model: HuggingFaceLLM):
        self.model = model


    def invoke(self, prompt: str, max_tokens: Optional[int] = 100) -> str:
        return self.model.complete(prompt, max_tokens=max_tokens)

    # def complete_many(self, prompts: List[str], max_tokens: Optional[int] = 100) -> List[str]:
    #     return self.model.complete_many(prompts, max_tokens=max_tokens)
