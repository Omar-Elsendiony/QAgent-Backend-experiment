from Imports import *
from utils.CustomThread import *


class TestGenerator:

    def __init__(self, GenUnitTestChain, db, data_JsonObj, myglobals, isHumanEval=True):
        self.reset()
        self.GenUnitTestChain = GenUnitTestChain
        self.db = db
        self.data_JsonObj = (
            data_JsonObj  # data json object , previously humanEval_JsonObj
        )
        self.myglobals = myglobals
        self.isHumanEval = isHumanEval

    def reset(self):
        self.fewshotsnum = 3
        self.isFewShot = True

    def generate(self, codeUnderTest, description):
        """
        This function is responsible for generating the test cases and running them
        It is the core of the TestGenerator class. It is responsible for:
        1. Extracting the code and description from the example
        2. Generating the test cases
        3. Running the test cases
        4. Storing the results in a JSON file
        Args: None
        Return: None
        """
        self.reset()
        fewShotStr = self.getExamplesFromDB(codeUnderTest)
        try:
            unittest = self.GenUnitTestChain.invoke(
                {
                    "description": description,
                    "code": codeUnderTest,
                    "test_cases_of_few_shot": "",  # fewShotStr # few shot str empty till RAG is implemented
                }
            )
        except Exception as e:
            print("ERROR in invoking GenUnitTestChain")

        unittestCode, isIncompleteResponse = getCodeFromResponse(unittest["text"], 0)
        if isIncompleteResponse:
            self.incompleteResponses += 1
            print(
                "Test Case Didn't Run Due to Incomplete Response\n=====================================\n"
            )
        feedback, feedbackparsed = self.runTest(codeUnderTest, unittestCode)
        print(feedbackparsed)

        NonSucceedingCasesNames = getNonSucceedingTestcases(feedback)
        NonSucceedingCasesNamesList = (
            NonSucceedingCasesNames["failed"] + NonSucceedingCasesNames["error"]
        )
        testsToRepeat = getEachTestCase(unittestCode, NonSucceedingCasesNamesList)
        return description, codeUnderTest, unittestCode, feedbackparsed, testsToRepeat

    def getExamplesFromDB(self, codeUnderTest):
        """
        Extract the few shot code and test cases from the database
        Args: code (str): The code of the example
        Return: fewShotStr (str): The few shot code and test cases
        """
        # get the few shot code and test cases
        codeOfFewShots, testCasesFewShots = getFewShots(self.db, codeUnderTest)
        # take the most similar few shot other than the code itself
        codeOfFewShots = codeOfFewShots[1 : self.fewshotsnum]
        testCasesFewShots = testCasesFewShots[1 : self.fewshotsnum]
        fewShotStr = preprocessStringFewShot(codeOfFewShots, testCasesFewShots)
        return fewShotStr

    # def extractExampleInfo(self, example):
    #     # Extract the code and description from the example
    #     code = example["code"]
    #     description = example["description"]
    #     return code, description

    def runTest(self, codeUnderTest, unittestCode):
        """
        Run the test case after some preprocessing of the returned response
        """
        unittestCode = preprocessUnitTest(unittestCode)
        codeTobeRun = getRunningCode(codeUnderTest, unittestCode)
        feedback = runCode(codeTobeRun, self.myglobals)
        feedbackparsed = getFeedbackFromRun(feedback)
        return feedback, feedbackparsed
