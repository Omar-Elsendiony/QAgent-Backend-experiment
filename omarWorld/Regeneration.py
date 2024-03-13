import re

class Regeneration:

    def __init__(self, chat_model) -> None:
        self.chat_model_arb = chat_model

    def regeneratePrompt(self, code, description, testcase):
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

        res = (self.chat_model_arb.invoke(reGenerationPrompt))
        if (res):
            res = res.content
        return res

    # made according to mixtral response
    def get_code_from_response(self, response):
        # has backticks in different positions
        s  = re.finditer(r"```python", response)
        for st in s:
            startIndex = st.span(0)[0]
        response = response[startIndex:]

        code = re.search(r"[^\"](?<=```python\n)(.*)\)\n(?=```)", response, re.DOTALL)
        if code is None:
            code = re.search(r"[^\"](?<=```python\n)(.*)\)\n\n(?=```)", response, re.DOTALL)
        if code is None:
            code = re.search(r"[^\"](?<=```python\n)(.*)\)(?=```)", response, re.DOTALL)
        if code is None:
            code = re.search(r"[^\"](?<=```python\n)(.*)", response, re.DOTALL)
        # print(code.group(0))
        if (code is None): return(response[startIndex:])
        return code.group(0) if code is not None else None

    def getTestCase(self,splitLines, errorChunck):
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

    def get_feedback(self, description, code, codeRan, feedback_test, get_feedback_from_run_list):
        def substituteTestCases(old, new, codeRan):
            new = re.sub(r"\n {4}([^d ])", r"\n        \1", new)
            new = re.sub(r"with(.*)\n {8}([^s|w])", r"with\1\n            \2", new)
            if (not new.startswith(" ")):
                new = "    " + new
            codeRan = re.sub(rf"{re.escape(old)}", rf"{new}", codeRan)
            return codeRan
        
        splitLines = codeRan.split('\n')
        feedback_l = get_feedback_from_run_list(feedback_test)
        if (feedback_l is None):
            return None
        # if (i == 2):
        #     print(codeRan)
        # print("================================")
        for f in feedback_l:
            # print("before:")
            before = self.getTestCase(splitLines, f)
            # print(before)
            # print("after: ")
            afterX = self.regeneratePrompt(code, description, before)
            after = self.get_code_from_response(afterX)
            matched = re.search(r'def test', after, re.DOTALL)
            # if (matched is None):
            #     print(afterX)
            #     continue
            start = matched.span()[0]
            matched = re.search(r'```', after, re.DOTALL)
            if (matched is None):
                after = after[start:]
            else:
                after = after[start:matched.span()[0]]
            # print(after)
            codeRan = substituteTestCases(before, after, codeRan)
        return codeRan


