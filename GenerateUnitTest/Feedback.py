from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_community.llms import HuggingFaceHub
import openai
from utils.PreprocessUtils import add_Mixtral_Tokens

RegenerateTestTemplate = """You are a Python expert, and your task is to debug and improve the following Python code based on the given description, code snippet, and unit tests feedback:

*Description:*
{description}

*Given Code:*
```python
{code}```
You previously generated the following code as unit tests:

python
```python
{UnitTests}```

After running the code with these tests, you received the following feedback based on the test output:
Feedback:
{Feedback}

Your goal is to revise the code or tests based on the feedback. Ensure to:

Address all highlighted bugs in the feedback.
Modify only the unit tests
Do not include new imports for the code or tests.
Preserve all existing functionality not related to the bugs.

Return your revised code or unit tests as only one formatted markdown code snippet without further explanation, surrounded by triple backticks and the word 'python'."""


# TODO: Change only one


def InitializeFeedbackChain(llm):
    global RegenerateTestTemplate
    # adding [INST] to mixtral manually
    if isinstance(llm, HuggingFaceHub) and "Mixtral" in llm.repo_id:
        RegenerateTestTemplate = add_Mixtral_Tokens(RegenerateTestTemplate)

    Generate_Unit_Tests_Template = PromptTemplate(
        template=RegenerateTestTemplate,
        input_variables=["description", "code", "UnitTests", "Feedback"],
        verbose=False,
    )
    GenUnitTestChain = LLMChain(
        llm=llm, verbose=False, prompt=Generate_Unit_Tests_Template
    )
    return GenUnitTestChain


def createPromptStringFeedback(description, code, UnitTests, Feedback):
    prompt = RegenerateTestTemplate.format(
        description=description, code=code, UnitTests=UnitTests, Feedback=Feedback
    )
    return prompt


def queryGptFeedback(model, description, code, UnitTests, Feedback):
    prompt = createPromptStringFeedback(description, code, UnitTests, Feedback)
    response = openai.ChatCompletion.create(
        model=model, messages=[{"role": "user", "content": prompt}]
    )

    return response
