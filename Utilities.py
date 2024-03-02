import re


def extract_function_name(string):
    # Define a regular expression pattern to match the function name
    pattern = r"def\s+(\w+)\s*\(.*\)"

    # Use re.match() to search for the pattern in the string
    match = re.match(pattern, string)

    # If a match is found, return the function name
    if match:
        return match.group(1)
    else:
        return None


# gets the function name from the function definition in human eval
def get_function_name(funcDefiniton):
    rs = re.search(r"\"\"\".*\"\"\"", funcDefiniton, re.DOTALL)
    if rs==None:
        rs = re.search(r"\'\'\'.*\'\'\'", funcDefiniton, re.DOTALL) 
    end = rs.span()[0]
    funcDefiniton = funcDefiniton[:end]
    return funcDefiniton


def replace_function_name(string, replacement_string):
    # Define the regular expression pattern to match the function name
    pattern = r"def\s+(\w+)\s*"

    # Use re.sub() to replace the pattern with the replacement string
    modified_string = re.sub(pattern, "def " + replacement_string, string)

    return modified_string


# made according to mixtral response
def get_code_from_response(response):
    # lines = response.split("\n")
    # code = ""
    # in_code = False
    # for i, line in enumerate(lines):
    #     if line.startswith("```python"):
    #         in_code = True
    #     elif line.startswith("```"):
    #         in_code = False
    #         return code
    #     elif in_code == True:
    #         if i == len(lines) - 1:
    #             return code
    #         code += line + "\n"
    # # incomplete output, most likely incomplete assertion.
    # # ignore this last assertion and move with the rest

    # return code
    # Omar: handles the cases where there are multiple python codes and where the response
    # has backticks in different positions
    code = re.search(r"[^\"](?<=```python\n)(.*)\)\n(?=```)", response, re.DOTALL)
    if code is None:
        code = re.search(r"[^\"](?<=```python\n)(.*)\)\n\n(?=```)", response, re.DOTALL)
    if code is None:
        code = re.search(r"[^\"](?<=```python\n)(.*)\)(?=```)", response, re.DOTALL)
    # print(code.group(0))
    return code.group(0)


# preprocesses the prompt string to be used in the few shot learning
def preprocessStringFewShot(code, unittest):
    string_few_shot = ""
    code_prepend = "# Code of a similar function \n'''python\n"
    test_case_prepend = "# Example unit tests for the similar code \n'''python\n"
    code_append = test_case_append = "'''\n"
    for i in zip(code, unittest):
        string_few_shot += (
            code_prepend
            + i[0]
            + code_append
            + test_case_prepend
            + i[1]
            + test_case_append
        )
    return string_few_shot


# gets feedback from running the code using exec
def get_feedback_from_run(response):
    lines = response.split("\n")
    feedback = ""
    in_failmessage = False
    for i, line in enumerate(lines):
        if line.startswith("FAIL") or line.startswith("ERROR"):
            in_failmessage = True
            feedback += line + "\n"
        elif line.startswith("--"):
            if lines[i + 1].startswith("Ran"):
                return feedback

        elif in_failmessage == True:
            if line.startswith("=="):
                continue
            if i == len(lines) - 1:
                return feedback
            feedback += line + "\n"


def get_feedback_from_run_list(response):  # omar's version
    lines = response.split("\n")
    in_failmessage = False
    feedbacks = []
    for i, line in enumerate(lines):
        if line.startswith("FAIL") or line.startswith("ERROR"):
            feedback = ""
            in_failmessage = True
            feedback += line + "\n"
        elif line.startswith("--"):
            if lines[i + 1].startswith("Ran"):
                if feedback != "":
                    feedbacks.append(feedback)
                return feedbacks

        elif in_failmessage == True:
            if line.startswith("=="):
                if feedback != "":
                    feedbacks.append(feedback)
                    feedback = ""
                    continue
            if i == len(lines) - 1:
                if feedback != "":
                    feedbacks.append(feedback)
                return feedbacks
            feedback += line + "\n"


# replaces the unittest call with another one to fix exec problem with running on colab
def replaceUnitTestCall(code):
    pattern = r"unittest.main()"

    # Use re.sub() to replace the pattern with the replacement string
    modified_code = re.sub(
        pattern, "unittest.main(argv=['first-arg-is-ignored'])", code
    )

    return modified_code


# def get_feedback_from_run(response):
#     lines = response.split("\n")
#     feedback = ""
#     in_failmessage = False
#     for i, line in enumerate(lines):
#         if line.startswith("FAIL"):
#             in_failmessage = True
#             feedback += line + "\n"
#         elif line.startswith("--"):
#             if lines[i + 1].startswith("Ran"):
#                 return feedback

#         elif in_failmessage == True:
#             if line.startswith("=="):
#                 continue
#             if i == len(lines) - 1:
#                 return feedback
#             feedback += line + "\n"
