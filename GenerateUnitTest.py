from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

GenerateTestTemplate = """Given the following description and python code:
Description:
{description}
Code:
{code}

Generate a class that contains multiple unit tests written in python to find bugs, syntax errors or logical errors in the code to conform with the description and include any required imports."""

Gen_UnitTest_with_FewShots_template = """Task: Given the following description and python code:

  Description:
  {description}
  Code:
  '''python
  {code}'''

  Generate a class that contains multiple unit tests written in python to find bugs, syntax errors or logical errors in the code to conform with the description and include any required imports.
  You are given example unit tests of a similar code from a database:
  '''python
  {test_cases_of_few_shot}'''


  Generate a class that contains multiple unit tests written in python to find bugs, syntax errors or logical errors in the code to conform with the description and include any required imports.
  The output should be a markdown code snippet formatted in the following schema, including the leading and trailing "```python" and "```":"""


def InitializeTestChain(chat_model):
    Generate_Unit_Tests_Template = PromptTemplate(
        template=Gen_UnitTest_with_FewShots_template,
        input_variables=["description", "code", "test_cases_of_few_shot"],
        verbose=True,
    )

    GenUnitTestChain = LLMChain(
        llm=chat_model, verbose=True, prompt=Generate_Unit_Tests_Template
    )
    return GenUnitTestChain
