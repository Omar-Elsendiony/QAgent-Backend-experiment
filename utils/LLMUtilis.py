import re


# made according to mixtral response
def get_code_from_response(response):
    incompleteResponse = False

    s  = re.finditer(r"```python", response)
    for st in s:
        startIndex = st.span(0)[0]
    response = response[startIndex:]

    code_match = re.search(r"[^\"](?<=```python\n)(.*)\)\n(?=```)", response, re.DOTALL)
    if code_match is None:
        code_match = re.search(
            r"[^\"](?<=```python\n)(.*)\)\n\n(?=```)", response, re.DOTALL
        )
    if code_match is None:
        code_match = re.search(
            r"[^\"](?<=```python\n)(.*)\)(?=```)", response, re.DOTALL
        )
    if code_match is None:
        code_match = re.search(r"[^\"](?<=```python\n)(.*)", response, re.DOTALL)
        # incomplete response, add to count
        incompleteResponse = True
    # code = code_match.group(0)
    # check if there is import for function under testand remove it

    # header="import "+funcDefiniton
    # if header in code:
    if (code_match is None): return(response[startIndex:], True)
    code = re.sub("from.*(?=class)", "", code_match.group(0), flags=re.DOTALL)
    return code, incompleteResponse


def regeneratePrompt(chat_model_arb, code, description, testcase):
    reGenerationPrompt = f"""
    you generated unittest for the following method under test having the following description:
    *Method under test*:
    {code}

    *Description*:
    {description}


    but this test failed
    *Test*:
    {testcase}


    Preserve the indentation correctness in the response
    fix only the unit test and re-run the code. The code should pass the test after the fix and enclosed by ```python and ``` to be able to run the code
    """

    res = (chat_model_arb.invoke(reGenerationPrompt)).content
    return res