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
        ExtractedResponse = response[startIndex:]
        if (
            "Your goal is to revise the code or tests based on the feedback. Ensure to:"
            in ExtractedResponse
        ):
            continue
        else:
            break
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


# extract test cases code according to given function names
def getEachTestCase(UnitTestsCode, functionNames):
    # split the test cases
    if len(functionNames) == 0:
        return UnitTestsCode
    classHeader = re.search(r"(class.*:)", UnitTestsCode)
    method_pattern = r"""
    (def\s+        # Match 'def' keyword followed by whitespace
    ({0})         # Capture method signature using a named capturing group (1) 
                   #  where {0} is replaced with the joined method names
    \(.*?\)     
    \s*:)\n        # Match whitespace, colon, and whitespace
    (.*?)          # Capture method body (non-greedy) - group (3)
    (?=\n\s*def|\n\Z) # Positive lookahead to ensure not followed by another 'def' or end of string
    """.format(
        "|".join(functionNames)
    )  # Replace {0} with joined method names
    tests = []
    matches = re.finditer(
        method_pattern, UnitTestsCode, flags=re.DOTALL | re.MULTILINE | re.VERBOSE
    )
    for functionmatch in matches:
        method_defintion = functionmatch.group(1)
        method_body = functionmatch.group(3)
        method_body_lines = method_body.split("\n")
        method_body = "\n".join(["\t" + line for line in method_body_lines])
        tests.append("\t" + method_defintion + "\n" + method_body)
    tests = "\n".join(tests)
    editPattern = """if __name__ == '__main__':"""
    index = tests.find(editPattern)
    if index != -1:
        mainCall = tests[index:]
        mainCall_lines = mainCall.split("\n")
        mainCall = "\n" + mainCall_lines[0] + "\n\t" + mainCall_lines[1].strip()
        tests = tests[:index] + mainCall  # Slice up to the index of the substring
    code = "\nimport unittest\n\n" + classHeader.group(0) + "\n" + tests
    return code


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
