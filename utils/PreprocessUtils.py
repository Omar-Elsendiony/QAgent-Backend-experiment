##### This file contains the utility functions for preprocessing string for either fewshot or running the code. ######
import re


# adds Mixtral Special Tokens to the prompt in case of vanilla llm by API
def add_Mixtral_Tokens(template):
    return "<s> [INST] " + template + "</s> [/INST]"


# made according to human eval
def remove_metadata(unittests):
    output = []
    for unitest in unittests:
        # pattern = re.compile(r"\bMETADATA\b\s*=\s*{.*}", re.DOTALL)

        # Use the sub() method to remove the matched block
        modified_unit_test = re.sub(
            "METADATA\s*=\s*\{([^}]*)\}", "", unitest, re.DOTALL
        ).lstrip("\n")
        output.append(modified_unit_test)
    return output


# preprocesses the prompt string to be used in the few shot learning
def preprocessStringFewShot(codes, example_unit_tests):

    string_few_shot = ""
    string_few_shot += '{\n"examples": ['
    open_curly = "{"
    close_curly = "}"
    index = 0
    code_prepend = " \"Code \n'''python\n"
    test_case_prepend = " \"Example unit tests \n'''python\n"
    code_append = test_case_append = "'''\n\""

    for i in zip(codes, example_unit_tests):
        index += 1
        string_few_shot += (
            open_curly
            + f'"input {index}":'
            + code_prepend.format(index=index)
            + i[0]
            + code_append
            + f', "output {index}":'
            + test_case_prepend.format(index=index)
            + i[1]
            + test_case_append
            + "},\n"
        )
    # remove the last comma
    string_few_shot = string_few_shot[:-2]
    string_few_shot += "]\n}"
    return string_few_shot


# replaces the unittest call with another one to fix exec problem with running on colab
def replaceUnitTestCall(code):
    pattern = r"unittest.main()"

    # Use re.sub() to replace the pattern with the replacement string
    modified_code = re.sub(
        pattern, "unittest.main(argv=['first-arg-is-ignored'])", code
    )

    return modified_code


introCode = """
import sys
import re
sys.setrecursionlimit(100)
"""


def get_running_code(code, unittest_code):
    global introCode
    runningCode = introCode + "\n" + code + "\n" + unittest_code
    return runningCode
