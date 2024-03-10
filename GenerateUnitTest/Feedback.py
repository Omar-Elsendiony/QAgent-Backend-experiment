from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_community.llms import HuggingFaceHub
import openai
from utils.PreprocessUtils import add_Mixtral_Tokens

RegenerateTestTemplate = """You are a python expert and your task is: Given the following description and python code:
  Description:
  {description}
  Code:
  '''python
  {code}'''
  You Previously Generated the Following code as unit tests:
  '''python
  {UnitTests}'''
  and after running the code this was the output of the tests:
  {Feedback}
  Use the Feedback to fix the bugs that are highlighted in the feedback by either modifying the code or the unit tests.
  Make sure to include the unit test call unittest.main() to run the tests. Do not include any import for the code under test.
  The output should be a markdown code snippet formatted in the following schema, including the leading and trailing "```python" and "```" respectively:"""


def InitializeFeedbackChain(llm):
    global RegenerateTestTemplate
    # adding [INST] to mixtral manually
    if isinstance(llm, HuggingFaceHub) and "Mixtral" in llm.repo_id:
        RegenerateTestTemplate = add_Mixtral_Tokens(RegenerateTestTemplate)

    Generate_Unit_Tests_Template = PromptTemplate(
        template=RegenerateTestTemplate,
        input_variables=["description", "code"],
        verbose=False,
    )
    GenUnitTestChain = LLMChain(
        llm=llm, verbose=False, prompt=Generate_Unit_Tests_Template
    )
    return GenUnitTestChain


def createPromptString(description, code, fewshots=False, test_cases_of_few_shot=None):
    prompt = RegenerateTestTemplate.format(description=description, code=code)
    return prompt


def queryGpt(model, description, code, fewshots=False, test_cases_of_few_shot=None):
    prompt = createPromptString(description, code, fewshots, test_cases_of_few_shot)
    response = openai.ChatCompletion.create(
        model=model, messages=[{"role": "user", "content": prompt}]
    )

    return response
