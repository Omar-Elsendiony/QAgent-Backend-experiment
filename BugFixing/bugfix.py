from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_community.llms import HuggingFaceHub
from langchain_community.chat_models.huggingface import ChatHuggingFace
import openai
from utils.PreprocessUtils import addMixtralTokens


repair_code_template = """You are a python expert in solving bugs:
Given the following python code, its description, a test case that produce an error, the error message and an explanation of a judge why the error is in the code under test.
knowing that a fair judge decided that the python code under test is buggy.
You are required to repair the code under test to be bugless and make sure that the functionality conform with the description provided.

Method under test:
{code}

Description:
{description}

test case that produces an error:
{test_case_error}

the error message:
{error_message}

Explanation of a judge why the error is in the code under test:
{explanation}

You follow my rules and orders and if you do not know the answer, don't make things UP!
You are going to follow the criteria that I give to you.
Criteria:
1. Understand the description and the python code under test.
2. Interpret the test case that produces an error and the accompanying error message.
3. Understand the explanation of a judge for why the error is in the code under test.
3. Repair the code under test to be bug-free.
4. make sure that the functionality of the repaired code conforms to the description.

Your answer is a list of bugs found and the repaired code only.
The repaired code should be a markdown code snippet formatted in the following schema, including the leading and trailing "```python" and "```" respectively:"""

Judge_template = """You are python unit tester judge. Given the following python code, its description, a test case that produce an error and the error message.
You are going to follow the criteria that I give to you.
You follow my rules and orders and if you do not know the answer, don't make things UP!
Criteria:
1. Understand the description and the python code under test.
2. Interpret the test case that produces an error and the accompanying error message.
3. Identify wether the error produced when excuting the test case is due to a bug in the python code under test or in the test case itself.
4. Provide a clear explanation for your decision.
Follow the provided criteria to make an informed decision.

Method under test:
{code}

Description:
{description}

test case that produces an error:
{test_case_error}

the error message:
{error_message}


Please thoroughly analyze the provided information before making your decision. Consider inspecting relevant portions of the code and test case, and provide a reasoned explanation for your conclusion.
I am going to to give you a template for your output where:
1- Replace **IS_METHOD_UNDER_TEST_BUGGY** with True or False based on your evaluation. 
2- Replace **EXPLANATION** with your explanation.
My template is:
Bug in the python code under test: **IS_METHOD_UNDER_TEST_BUGGY**
Explanation: **EXPLANATION**
Remember you are a judge and you should be fair and just. Do not make things up. Think before you end the response. I do not want any incomplete response.
"""


