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
def get_code_from_response(response,funcDefiniton):
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
    if code is None:
        code = re.search(r"[^\"](?<=```python\n)(.*)", response, re.DOTALL)
    # print(code.group(0))
    true_code=code.group(0)
    #check if there is import for function under testand remove it
    
    # header="import "+funcDefiniton
    # if header in true_code:
    final_code = re.sub("from.*(?=class)", "", true_code, flags=re.DOTALL)

        # return final_code
    return final_code

def remove_metadata(unittests):
    output = []
    for unitest in unittests:
        #pattern = re.compile(r"\bMETADATA\b\s*=\s*{.*}", re.DOTALL)

        # Use the sub() method to remove the matched block
        modified_unit_test = re.sub("METADATA\s*=\s*\{([^}]*)\}","", unitest,re.DOTALL).lstrip('\n')
        output.append(modified_unit_test)
    return output

# preprocesses the prompt string to be used in the few shot learning
def preprocessStringFewShot(code, unittest):
    example_unit_tests=remove_metadata(unittest)

    string_few_shot = ""
    string_few_shot +="{\n\"examples\": ["
    open_curly = "{"
    close_curly = "}"
    index=0
    code_prepend = " \"Code \n'''python\n"
    test_case_prepend = " \"Example unit tests \n'''python\n"
    code_append = test_case_append = "'''\n\""
    
    for i in zip(code, example_unit_tests):
        index+=1
        string_few_shot += (
            open_curly
            +f"\"input {index}\":"
            +code_prepend.format(index=index)
            + i[0]
            + code_append
            +f", \"output {index}\":"
            + test_case_prepend.format(index=index)
            + i[1]
            + test_case_append
            + "},\n"
        )
    #remove the last comma
    string_few_shot = string_few_shot[:-2]
    string_few_shot +="]\n}"
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
