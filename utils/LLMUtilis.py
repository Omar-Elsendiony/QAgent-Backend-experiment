import re


# made according to mixtral response
def get_code_from_response(response):
    incompleteResponse = False

    s = re.finditer(r"```python", response)
    ExtractedResponse = ""
    for st in s:
        # pick a statement from the prompt template and ensure it's no in the chosen repsonse
        startIndex = st.span(0)[0]
    ExtractedResponse = response[startIndex:]

    code_match = re.search(
        r"[^\"](?<=```python\n)(.*)\)\n(?=```)", ExtractedResponse, re.DOTALL
    )
    if code_match is None:
        code_match = re.search(
            r"[^\"](?<=```python\n)(.*)\)\n\n(?=```)", ExtractedResponse, re.DOTALL
        )
    if code_match is None:
        code_match = re.search(
            r"[^\"](?<=```python\n)(.*)\)(?=```)", ExtractedResponse, re.DOTALL
        )
    if code_match is None:
        code_match = re.search(
            r"[^\"](?<=```python\n)(.*)", ExtractedResponse, re.DOTALL
        )
        # incomplete response, add to count
        incompleteResponse = True
    # code = code_match.group(0)
    # check if there is import for function under testand remove it

    # header="import "+funcDefiniton
    # if header in code:
    if code_match is None:
        return (response[startIndex:], True)
    code = re.sub("from.*(?=class)", "", code_match.group(0), flags=re.DOTALL)
    return code, incompleteResponse


def get_code_from_feedbackresponse(response):
    incompleteResponse = False

    s = re.finditer(r"```python", response)
    ExtractedResponse = ""
    for st in s:
        # pick a statement from the prompt template and ensure it's no in the chosen repsonse
        startIndex = st.span(0)[0]
        print("Start Index is ", startIndex)
        ExtractedResponse = response[startIndex:]
        print("Response is ", ExtractedResponse)
        if (
            "Your goal is to revise the code or tests based on the feedback. Ensure to:"
            in ExtractedResponse
        ):
            continue
        else:
            break
    print("Extracted Response is ", ExtractedResponse)
    code_match = re.search(
        r"[^\"](?<=```python\n)(.*)\)\n(?=```)", ExtractedResponse, re.DOTALL
    )
    if code_match is None:
        code_match = re.search(
            r"[^\"](?<=```python\n)(.*)\)\n\n(?=```)", ExtractedResponse, re.DOTALL
        )
    if code_match is None:
        code_match = re.search(
            r"[^\"](?<=```python\n)(.*)\)(?=```)", ExtractedResponse, re.DOTALL
        )
    if code_match is None:
        code_match = re.search(
            r"[^\"](?<=```python\n)(.*)", ExtractedResponse, re.DOTALL
        )
        # incomplete response, add to count
        incompleteResponse = True
    # code = code_match.group(0)
    # check if there is import for function under testand remove it

    # header="import "+funcDefiniton
    # if header in code:
    if code_match is None:
        return (response[startIndex:], True)
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
