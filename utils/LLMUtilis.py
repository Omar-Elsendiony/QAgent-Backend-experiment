import re


# made according to mixtral response
def get_code_from_response(response):
    incompleteResponse = False
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
    code = code_match.group(0)
    # check if there is import for function under testand remove it

    # header="import "+funcDefiniton
    # if header in code:
    code = re.sub("from.*(?=class)", "", code, flags=re.DOTALL)
    return code, incompleteResponse
