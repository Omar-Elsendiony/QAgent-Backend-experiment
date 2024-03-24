from Imports import *
from CustomThread import *
from GenerateUnitTest.Regeneration import *


class TestFix:

    def __init__(self, myglobals):
        self.reset()
        self.myglobals = myglobals
        llm_arb, chat_model_arb = InitializeModelArbiter(os.environ["HF_TOKEN"])
        self.reg = Regeneration(chat_model_arb)

    def reset(self):
        self.totalTestCasesNum = 0
        self.totalSuccessTestCasesNum = 0
        self.failed_test_cases = 0
        self.error_test_cases = 0
        self.failedExamplesNum = 0
        self.successfulExamplesNum = 0
        self.apiErrors = 0
        self.testsToRepeat = 0  # Number of tests to repeat = Summation of all tests under failed examples whether they are failed or succeeded
        self.OKCases = 0
        self.descriptions = []
        self.codes = []
        self.resCodes = []
        self.feedbacks = []
        self.codeRanList = []
        self.TotalCases = 0
        self.TotalFailedCases = 0
        self.incompleteResponses = 0
        self.OutputFile = "FeedbackOutput/"
        self.JSONFile = self.OutputFile + "RunningLogs.json"
        self.CasesJSONFile = self.OutputFile + "Cases.json"
        OldFile = "Results/FeedbackMixtral-2Shot/"
        self.OldCasesFile = OldFile + "Cases.json"
        self.OldJsonFile = OldFile + "RunningLogs.json"
        self.CasesLogs = pd.read_json(self.OldJsonFile)
        self.OldCases = pd.read_json(self.OldCasesFile)
        self.df = pd.DataFrame()
        self.casesDf = pd.DataFrame()

    def generate(self):
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
        self.checkPaths()
        self.reset()
        c = open(self.OutputFile + "Cases.txt", "w+")
        for i in range(0, 3):
            print("Running Example ", i, "\n=====================\n")

            currDescription, currCode, currGeneratedCode, currFeedback = (
                self.extractInfo(i)
            )
            currRanCode = getRunningCode(currCode, currGeneratedCode)

            if pd.isna(currFeedback) or currFeedback == "" or currFeedback is None:
                print("Example", i, " has already passed")
                c.write(
                    "Example "
                    + str(i)
                    + " has already passed\n=====================================\n"
                )
                continue
            try:
                codeTobeRun = self.reg.get_feedback(
                    currDescription,
                    currCode,
                    currRanCode,
                    currFeedback,
                    getFeedbackFromRunList,
                )
                if codeTobeRun is not None:
                    codeTobeRun = replaceUnitTestCall(codeTobeRun)
                    feedback = runCode(code=codeTobeRun, myglobals=self.myglobals)
                    print("original feedback is: ", feedback)
                    feedbackparsed = getFeedbackFromRun(feedback)
                    unittestCode = codeTobeRun[
                        (re.search(r"import unittest", codeTobeRun)).span()[0] :
                    ]
                else:
                    self.incompleteResponses += 1
                    continue
            except Exception as e:
                print("ERROR in invoking Feedback Chain")
                self.apiErrors += 1
                print(e)
                c.write(
                    "Example "
                    + str(i)
                    + " Didn't Run Due to Errorr\n=====================================\n"
                )
                continue

            self.writeResults(feedback, feedbackparsed, unittestCode, c, i)
            self.descriptions.append(currDescription)
            self.codes.append(currCode)
            self.resCodes.append(unittestCode)
            self.feedbacks.append(feedbackparsed)  # feedbackparsed
            # codeRanList.append(codeTobeRun)
            newRow = pd.DataFrame(
                {
                    "CaseNumber": i,
                    "Description": currDescription,
                    "Code": currCode,
                    "GeneratedCode": unittestCode,
                    "CodeRan": codeTobeRun,
                    "Feedback": feedbackparsed,
                    "FullFeedback": feedback,
                    # "TestsToRepeat": testsToRepeat,
                },
                index=[0],
            )
            # df = df.append(newRow, ignore_index=True)
            self.df = pd.concat([self.df, newRow])
            # Save the updated DataFrame back to the excel file using 'openpyxl' engine for writing
            jsondata = self.df.to_dict(orient="records")
            with open(self.JSONFile, "w") as f:
                json.dump(jsondata, f, indent=4)

        self.printResults()
        c.close()
        return

    def extractInfo(self, i):
        """
        Extract the description and code from the example in addition to prepending the function header
        Args: i (int): The index of the example in the JSON file
        Return: description (str): The description of the example
                code (str): The code of the example
                generatedCode (str): The generated code of the example
                feedback (str): The feedback of the example
        """
        currDescription = self.CasesLogs.iloc[i]["Description"]
        currCode = self.CasesLogs.iloc[i]["Code"]
        currGeneratedCode = self.CasesLogs.iloc[i]["GeneratedCode"]
        currFeedback = self.CasesLogs.iloc[i]["Feedback"]

        return currDescription, currCode, currGeneratedCode, currFeedback

    def checkPaths(self):
        """
        Check if these directories and files exist, if not create them
        Args: None
        Return: None
        """
        if not os.path.exists(self.CasesJSONFile):
            try:
                # Create a new empty JSON file with an empty list structure
                with open(self.CasesJSONFile, "w") as f:
                    json.dump([], f)
                print(f"File {self.CasesJSONFile} created successfully!")
            except Exception as e:
                print(f"Error creating file {self.CasesJSONFile}: {e}")
                exit()

        if not os.path.exists(self.JSONFile):
            try:
                # Create a new empty JSON file with an empty list structure
                with open(self.JSONFile, "w") as f:
                    json.dump([], f)
                    print(f"File {self.JSONFile} created successfully!")
            except Exception as e:
                print(f"Error creating file {self.JSONFile}: {e}")
                exit()

    def writeResults(self, feedback, feedbackparsed, unittestCode, c, i):
        """
        Responsible for writing results to cases.txt and cases.json

        Args: feedbackparsed (str): The parsed feedback from the test case


        """
        numOfAssertions = getNumAssertions(unittestCode)
        if feedbackparsed == "" or feedbackparsed is None:
            # in case of OK
            self.successfulExamplesNum += 1
            self.OKCases += 1
            print(
                f"Test example {i} succeeded\n======================================\n"
            )
            print("Number of Ran Tests : ", numOfAssertions)
            print("Number of Succeeded Test : ", numOfAssertions)
            print("Number of Succeeded Test : ", 0)
            c.write("Test example " + str(i) + " succeeded\n")
            c.write("Number of Ran Tests : " + str(numOfAssertions) + "\n")
            c.write("Number of Succeeded Test : " + str(numOfAssertions) + "\n")

            oldTotalTests = self.OldCases.iloc[i]["Total Tests"]
            oldTestsFailed = self.OldCases.iloc[i]["Tests failed"]
            oldTestsError = ""
            print("Old Error Tests", oldTestsError)

            newCaseRow = pd.DataFrame(
                {
                    "CaseNumber": i,
                    "Feedback Total Tests": numOfAssertions,
                    "Feedback Tests failed": 0,
                    "Feedback Error Tests": 0,
                    "Old Total Tests": oldTotalTests,
                    "Old Tests Failed": oldTestsFailed,
                    "Old Tests Error": oldTestsError,
                },
                index=[0],
            )
            self.casesDf = pd.concat([self.casesDf, newCaseRow])
            casejsondata = self.casesDf.to_dict(orient="records")
            with open(self.CasesJSONFile, "w") as f:
                json.dump(casejsondata, f, indent=4)

            self.totalTestCasesNum += numOfAssertions

        else:
            self.failedExamplesNum += 1
            failedCasesNum, errorCasesNum = getNumNonSucceedingTestcases(feedback)
            NonSucceedingCasesNames = getNonSucceedingTestcases(feedback)
            NonSucceedingCasesNamesList = (
                NonSucceedingCasesNames["failed"] + NonSucceedingCasesNames["error"]
            )
            testsToRepeat = getEachTestCase(unittestCode, NonSucceedingCasesNamesList)
            numberOfSucceeded = numOfAssertions - failedCasesNum - errorCasesNum
            print(f"Test example {i} failed\n======================================\n")
            print("Number of Ran Tests : ", numOfAssertions)
            print("Number of failed Tests : ", failedCasesNum)
            print("Number of error Tests : ", errorCasesNum)
            print(
                "Number of Succeeded Test : ",
                numberOfSucceeded,
            )
            c.write("Test example " + str(i) + " failed\n")
            c.write("Number of Ran Tests : " + str(numOfAssertions) + "\n")
            c.write("Number of failed Tests : " + str(failedCasesNum) + "\n")
            c.write("Number of Error Test : " + str(errorCasesNum) + "\n")
            c.write("Number of Succeeded Test : " + str(numberOfSucceeded) + "\n")

            oldTotalTests = self.OldCases.iloc[i]["Total Tests"]
            oldTestsFailed = self.OldCases.iloc[i]["Tests failed"]
            oldTestsError = ""
            print("Old Error Tests", oldTestsError)

            newCaseRow = pd.DataFrame(
                {
                    "CaseNumber": i,
                    "Feedback Total Tests": numOfAssertions,
                    "Feedback Tests failed": 0,
                    "Feedback Error Tests": 0,
                    "Old Total Tests": oldTotalTests,
                    "Old Tests Failed": oldTestsFailed,
                    "Old Tests Error": oldTestsError,
                },
                index=[0],
            )
            self.casesDf = pd.concat([self.casesDf, newCaseRow])
            casejsondata = self.casesDf.to_dict(orient="records")
            with open(self.CasesJSONFile, "w") as f:
                json.dump(casejsondata, f, indent=4)
            self.testsToRepeat += len(NonSucceedingCasesNamesList)
            self.totalTestCasesNum += numOfAssertions
            self.failed_test_cases += failedCasesNum
            self.error_test_cases += errorCasesNum

    def printResults(self):
        """
        Prints the remaining results and create Res.txt which includes a summary of the overall run

        """
        print("\n End of Test Cases \n")
        print("Total succeeded examples : ", self.successfulExamplesNum)
        print("Total failed examples : ", self.failedExamplesNum)
        print("Total  testcases : ", self.totalTestCasesNum)
        print(
            "Total succeeded testcases : ",
            self.totalTestCasesNum
            - self.failed_test_cases
            - self.incompleteResponses
            - self.error_test_cases,
        )
        print("Total failed testcases : ", self.failed_test_cases)
        print("Total error testcases : ", self.error_test_cases)
        print("Tests to repeat : ", self.testsToRepeat)
        print("Incomplete Responses are : ", self.incompleteResponses)
        print("API Errors are : ", self.apiErrors)
        with open(self.OutputFile + "Res.txt", "w") as f:
            f.write(
                "Total succeeded examples : " + str(self.successfulExamplesNum) + "\n"
            )
            f.write("Total failed examples : " + str(self.failedExamplesNum) + "\n")
            f.write("Total  testcases : " + str(self.totalTestCasesNum) + "\n")
            f.write(
                "Total succeeded testcases : "
                + str(
                    self.totalTestCasesNum
                    - self.failed_test_cases
                    - self.incompleteResponses
                    - self.error_test_cases
                    - self.apiErrors
                )
                + "\n"
            )
            f.write("Total failed testcases : " + str(self.failed_test_cases) + "\n")
            f.write("Total error testcases : " + str(self.error_test_cases) + "\n")
            f.write(
                "Incomplete Responses are : " + str(self.incompleteResponses) + "\n"
            )
            f.write("API Errors are : " + str(self.apiErrors) + "\n")
            f.write("Tests to repeat : " + str(self.testsToRepeat) + "\n")

        print("Incomplete Responses are ", self.incompleteResponses)
