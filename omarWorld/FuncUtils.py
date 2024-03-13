import re

introCode = """
import sys
import re
sys.setrecursionlimit(100)
"""

class FuncUtils:

    def extract_function_name(self, string):
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
    def get_function_name(self, funcDefinition):
        rs = re.search(r"\"\"\".*\"\"\"", funcDefinition, re.DOTALL)
        if rs == None:
            rs = re.search(r"\'\'\'.*\'\'\'", funcDefinition, re.DOTALL)
        
        allMatches = re.findall(r"def ", funcDefinition)
        if (len(allMatches) == 1):
            end = rs.span()[0]
            funcHeader = funcDefinition[:end]
            UtilityFunction = ""
        else:
            *_, last = re.finditer(r"def ", funcDefinition)
            begin = last.span()[0]
            secondPart = funcDefinition[begin:]
            rs = re.search(r"\"\"\".*\"\"\"", secondPart, re.DOTALL)
            if rs == None:
                rs = re.search(r"\'\'\'.*\'\'\'", secondPart, re.DOTALL)        
            end = rs.span()[0]
            funcHeader = funcDefinition[begin:end+begin]
            UtilityFunction = funcDefinition[:begin]
        return funcHeader, UtilityFunction


    # replace function name if needed
    def replace_function_name(self, string, replacement_string):
        # Define the regular expression pattern to match the function name
        pattern = r"def\s+(\w+)\s*"

        # Use re.sub() to replace the pattern with the replacement string
        modified_string = re.sub(pattern, "def " + replacement_string, string)

        return modified_string



    def getTestCase(self, splitLines, errorChunck):
        lineNoGroup = re.search(r'(?<=line )(\d)+', errorChunck)
        lineNo = lineNoGroup.group(0) #line number of the end of the error
        def getStartTestCase(splitLines, startIndex):
            for i in range(startIndex, 0, -1):
                if splitLines[i].find('def test') != - 1:
                    return i
            return -1
        startCaseIndex = getStartTestCase(splitLines, int(lineNo))
        testCase = "\n".join(splitLines[startCaseIndex:int(lineNo)])
        return testCase


    # adds Mixtral Special Tokens to the prompt in case of vanilla llm by API
    def add_Mixtral_Tokens(self, template):
        return "<s> [INST] " + template + "</s> [/INST]"


    # made according to human eval
    def remove_metadata(self, unittests):
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
    def preprocessStringFewShot(self, codes, example_unit_tests):

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
    def replaceUnitTestCall(self, code):
        pattern = r"unittest.main()"

        # Use re.sub() to replace the pattern with the replacement string
        modified_code = re.sub(
            pattern, "unittest.main(argv=['first-arg-is-ignored'])", code
        )

        return modified_code


    def addUnitTestImport(self, code):
        pattern = r"import unittest"

        ## search for the pattern in code and add it if not present
        if re.search(pattern, code):
            return code
        else:
            modified_code = "import unittest\n" + code
            return modified_code


    def preprocessUnitTest(self, code):
        code = self.replaceUnitTestCall(code)
        code = self.addUnitTestImport(code)
        return code

    def get_running_code(code, unittest_code):
        global introCode
        runningCode = introCode + "\n" + code + "\n" + unittest_code
        return runningCode


    # made according to mixtral response
    def get_code_from_response(self, response):
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


    def get_feedback_from_run(self, response):
        lines = response.split("\n")
        feedback = ""
        in_failmessage = False
        if lines[0].startswith("F") or lines[0].startswith(".") or lines[0].startswith("E"): # the added . for the test case that includes an error
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
            return feedback
        else:
            return response


    def get_feedback_from_run_list(self, response):  # omar's version
        lines = response.split("\n")
        in_failmessage = False
        feedbacks = []
        feedback = ""
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


    def get_failed_testcases(self, feedback):
        # Use a regular expression to find the number of Ran Tests and Failures
        ran_tests_match = re.search(r"Ran (\d+) tests", feedback)
        failures_match = re.search(r"failures=(\d+)", feedback)
        errors_match = re.search(r"errors=(\d+)", feedback)
        # Extract the numbers or default to 0 if not found
        ran_tests = int(ran_tests_match.group(1)) if ran_tests_match else 0
        failures = int(failures_match.group(1)) if failures_match else 0
        errors = int(errors_match.group(1)) if errors_match else 0

        return ran_tests, failures, errors


    def get_num_assertions(code_text):
        total_num = len(
            re.findall(r"self\.assert\w*\(.*?\)", code_text, flags=re.MULTILINE)
        )
        return total_num