import re


# adds Mixtral Special Tokens to the prompt in case of vanilla llm by API
def add_Mixtral_Tokens(template):
    return "<s> [INST] " + template + "</s> [INST]"


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


# replaces the unittest call with another one to fix exec problem with running on colab
def replaceUnitTestCall(code):
    pattern = r"unittest.main()"

    # Use re.sub() to replace the pattern with the replacement string
    modified_code = re.sub(
        pattern, "unittest.main(argv=['first-arg-is-ignored'])", code
    )

    return modified_code
