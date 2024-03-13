import re


# made according to mixtral response
def get_code_from_response(response):
    incompleteResponse = False

    s  = re.finditer(r"```python", response)
    for st in s:
        startIndex = st.span(0)[0]
    response = response[startIndex:]

    code_match = re.search(r"[^\"](?<=```python\n)(.*)\)\n(?=```)", response, re.DOTALL) # this is the basic case where it is not preceded by " and it is closed by ``` three backticks`
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


