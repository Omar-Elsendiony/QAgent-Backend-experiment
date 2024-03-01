from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

GenerateTestTemplate = """You are a python expert and your task is: Given the following description and python code:
  Description:
  {description}
  Code:
  '''python
  {code}'''
  Generate a class that contains at least 7 unit tests (where each test has only one assertion) written in python that acheive high coverage to find bugs, runtime errors or logical errors in the code to conform with the description and include any required imports.
  Make sure to include the unit test call unittest.main() to run the tests.
  The output should be a markdown code snippet formatted in the following schema, including the leading and trailing "```python" and "```" respectively:"""

Gen_UnitTest_with_FewShots_template = """You are a python expert and your task is: Given the following description and python code:
  Description:
  {description}
  Code:
  '''python
  {code}'''
  Generate a class that contains at least 7 unit tests (where each test has only one assertion) written in python that acheive high coverage to find bugs, runtime errors or logical errors in the code to conform with the description and include any required imports.
  You are given examples of unit tests for a similar code, which you can use to write the unit tests for the given code.:
  '''python
  {test_cases_of_few_shot}'''
  Make sure to include the unit test call unittest.main() to run the tests.
  The output should be a markdown code snippet formatted in the following schema, including the leading and trailing "```python" and "```" respectively:"""


def InitializeTestChain(chat_model, fewshots=False):
    if not fewshots:
        Generate_Unit_Tests_Template = PromptTemplate(
            template=GenerateTestTemplate,
            input_variables=["description", "code"],
            verbose=False,
        )
    else:
        Generate_Unit_Tests_Template = PromptTemplate(
            template=Gen_UnitTest_with_FewShots_template,
            input_variables=["description", "code", "test_cases_of_few_shot"],
            verbose=False,
        )

    GenUnitTestChain = LLMChain(
        llm=chat_model, verbose=False, prompt=Generate_Unit_Tests_Template
    )
    return GenUnitTestChain
