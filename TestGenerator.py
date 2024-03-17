from Imports import *
from CustomThread import *


class TestGenerator:

    def __init__(self, GenUnitTestChain, db, HEval_JsonObj, myglobals):
        self.reset()
        self.GenUnitTestChain = GenUnitTestChain
        self.db = db
        self.HEval_JsonObj = HEval_JsonObj
        self.myglobals = myglobals

    def reset(self):
        self.total_test_cases = 0
        self.total_success_test_cases = 0
        self.failed_test_cases = 0
        self.error_test_cases = 0
        self.num_failed_examples = 0
        self.num_successful_examples = 0
        self.testsToRepeat = 0  # Number of tests to repeat = Summation of all tests under failed examples whether they are failed or succeeded
        self.OKCases = 0
        self.descriptions = []
        self.codes = []
        self.res_codes = []
        self.feedbacks = []
        self.codeRanList = []
        self.TotalCases = 0
        self.TotalFailedCases = 0
        self.incompleteResponses = 0
        self.OutputFile = "OutputTest/"
        self.JSONFile = self.OutputFile + "RunningLogs.json"
        self.CasesJSONFile = self.OutputFile + "Cases.json"
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
        c = open(self.OutputFile + "Cases.txt", "w+")
        for i in range(0, 10):
            # if (i == 10): continue
            print("Running Test Case ", i)
            c.write(
                "Running Test Case "
                + str(i)
                + "\n=====================================\n"
            )
            # description and code from database
            description, code = self.extractInfo(i)
            fewShotStr = self.extractFewShots(code)
            try:
                unittest = self.GenUnitTestChain.invoke(
                    {
                        "description": description,
                        "code": code,
                        "test_cases_of_few_shot": fewShotStr,
                    }
                )  # ,"test_cases_of_few_shot":fewShotStr
            except Exception as e:
                print("ERROR in invoking GenUnitTestChain")
                print(e)
                c.write(
                    "Test Case "
                    + str(i)
                    + " Didn't Run Due to Errorr\n=====================================\n"
                )
                continue
            unittest_code, isIncompleteResponse = get_code_from_response(
                unittest["text"]
            )
            if isIncompleteResponse:
                self.incompleteResponses += 1
                print(
                    "Test Case "
                    + str(i)
                    + " Didn't Run Due to Incomplete Response\n=====================================\n"
                )
                c.write(
                    "Test Case "
                    + str(i)
                    + " Didn't Run Due to Incomplete Response\n=====================================\n"
                )
            feedback, feedbackparsed, codeTobeRun = self.runTest(code, unittest_code)
            print(feedbackparsed)

            self.writeResults(feedback, feedbackparsed, unittest_code, c, i)
            self.descriptions.append(description)
            self.codes.append(code)
            self.res_codes.append(unittest_code)
            self.feedbacks.append(feedbackparsed)  # feedbackparsed
            # codeRanList.append(codeTobeRun)
            new_row = pd.DataFrame(
                {
                    "CaseNumber": i,
                    "Description": description,
                    "Code": code,
                    "GeneratedCode": unittest_code,
                    "CodeRan": codeTobeRun,
                    "Feedback": feedbackparsed,
                    "FullFeedback": feedback,
                },
                index=[0],
            )
            # df = df.append(new_row, ignore_index=True)
            self.df = pd.concat([self.df, new_row])
            # Save the updated DataFrame back to the excel file using 'openpyxl' engine for writing
            jsondata = self.df.to_dict(orient="records")
            with open(self.JSONFile, "w") as f:
                json.dump(jsondata, f, indent=4)
        c.close()

        self.printResults()
        return

    def extractInfo(self, i):
        """
        Extract the description and code from the example in addition to prepending the function header
        Args: i (int): The index of the example in the JSON file
        Return: description (str): The description of the example
                code (str): The code of the example
        """
        description = self.HEval_JsonObj.iloc[i]["text"]
        code = self.HEval_JsonObj.iloc[i]["canonical_solution"]
        # current loop to remove initial spaces in extracted code
        indexer = 0
        while code[indexer] == " ":
            indexer += 1
        code = code[indexer:]
        # extract the function definition and utility code
        funcDefiniton = self.HEval_JsonObj.iloc[i]["prompt"]
        funcDefiniton, Utility = get_function_name(
            funcDefiniton
        )  # does not need entry point at the end of the day
        code = Utility + "\n" + funcDefiniton + code

        return description, code

    def extractFewShots(self, code):
        """
        Extract the few shot code and test cases from the database
        Args: code (str): The code of the example
        Return: fewShotStr (str): The few shot code and test cases
        """
        # get the few shot code and test cases
        codes_of_few_shot, test_cases_few_shot = get_few_shots(self.db, code)
        # take the most similar few shot other than the code itself
        codes_of_few_shot, test_cases_few_shot = (
            codes_of_few_shot[1:3],
            test_cases_few_shot[1:3],
        )
        fewShotStr = preprocessStringFewShot(codes_of_few_shot, test_cases_few_shot)
        return fewShotStr

    def checkPaths(self):
        """
        Check if these directories and files exist, if not create them
        Args: None
        Return: None
        """
        if not os.path.exists(self.OutputFile):
            try:
                os.makedirs(self.OutputFile)
                print(f"Directory {self.OutputFile} created successfully!")
            except Exception as e:
                print(f"Error creating directory {self.OutputFile}: {e}")
                exit()

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

    def extractExampleInfo(self, example):
        # Extract the code and description from the example
        code = example["code"]
        description = example["description"]
        return code, description

    def runTest(self, code, unittest_code):
        """
        Run the test case after some preprocessing of the returned response
        """
        unittest_code = preprocessUnitTest(unittest_code)
        # codeTobeRun = introCode + "\n" + code + "\n" + unittest_code
        codeTobeRun = get_running_code(code, unittest_code)
        # print("unittest_code is: \n ",unittest_code)
        # print("run_code is \n",codeTobeRun)
        feedback = runCode(codeTobeRun, self.myglobals)
        feedbackparsed = get_feedback_from_run(feedback)
        return feedback, feedbackparsed, codeTobeRun

    def writeResults(self, feedback, feedbackparsed, unittest_code, c, i):
        """
        Responsible for writing results to cases.txt and cases.json

        Args: feedbackparsed (str): The parsed feedback from the test case


        """
        num_of_assertions = get_num_assertions(unittest_code)
        if feedbackparsed == "" or feedbackparsed is None:
            # in case of OK
            self.num_successful_examples += 1
            self.OKCases += 1
            print(
                f"Test example {i} succeeded\n======================================\n"
            )
            print("Number of Ran Tests : ", num_of_assertions)
            print("Number of Succeeded Test : ", num_of_assertions)
            print("Number of Succeeded Test : ", 0)
            c.write("Test example " + str(i) + " succeeded\n")
            c.write("Number of Ran Tests : " + str(num_of_assertions) + "\n")
            c.write("Number of Succeeded Test : " + str(num_of_assertions) + "\n")
            new_case_row = pd.DataFrame(
                {"CaseNumber": i, "Total Tests": num_of_assertions, "Tests failed": 0},
                index=[0],
            )
            self.casesDf = pd.concat([self.casesDf, new_case_row])
            casejsondata = self.casesDf.to_dict(orient="records")
            with open(self.CasesJSONFile, "w") as f:
                json.dump(casejsondata, f, indent=4)

            self.total_test_cases += num_of_assertions

        else:
            self.num_failed_examples += 1
            failed_cases, error_cases = get_failed_testcases(feedback)
            print(f"Test example {i} failed\n======================================\n")
            print("Number of Ran Tests : ", num_of_assertions)
            print("Number of failed Tests : ", failed_cases)
            print("Number of error Tests : ", error_cases)
            print(
                "Number of Succeeded Test : ",
                num_of_assertions - failed_cases - error_cases,
            )
            c.write("Test example " + str(i) + " failed\n")
            c.write("Number of Ran Tests : " + str(num_of_assertions) + "\n")
            c.write("Number of failed Tests : " + str(failed_cases) + "\n")
            c.write(
                "Number of Succeeded Test : "
                + str(num_of_assertions - failed_cases - error_cases)
                + "\n"
            )
            c.write("Number of Error Test : " + str(error_cases) + "\n")
            new_case_row = pd.DataFrame(
                {
                    "CaseNumber": i,
                    "Total Tests": num_of_assertions,
                    "Tests failed": failed_cases,
                },
                index=[0],
            )
            self.casesDf = pd.concat([self.casesDf, new_case_row])
            casejsondata = self.casesDf.to_dict(orient="records")
            with open(self.CasesJSONFile, "w") as f:
                json.dump(casejsondata, f, indent=4)
            self.testsToRepeat += num_of_assertions
            self.total_test_cases += num_of_assertions
            self.failed_test_cases += failed_cases
            self.error_test_cases += error_cases

    def printResults(self):
        """
        Prints the remaining results and create Res.txt which includes a summary of the overall run

        """
        print("\n End of Test Cases \n")
        print("Total succeeded examples : ", self.num_successful_examples)
        print("Total failed examples : ", self.num_failed_examples)
        print("Total  testcases : ", self.total_test_cases)
        print(
            "Total succeeded testcases : ",
            self.total_test_cases
            - self.failed_test_cases
            - self.incompleteResponses
            - self.error_test_cases,
        )
        print("Total failed testcases : ", self.failed_test_cases)
        print("Total error testcases : ", self.error_test_cases)
        print("Tests to repeat : ", self.testsToRepeat)
        with open(self.OutputFile + "Res.txt", "w") as f:
            f.write(
                "Total succeeded examples : " + str(self.num_successful_examples) + "\n"
            )
            f.write("Total failed examples : " + str(self.num_failed_examples) + "\n")
            f.write("Total  testcases : " + str(self.total_test_cases) + "\n")
            f.write(
                "Total succeeded testcases : "
                + str(
                    self.total_test_cases
                    - self.failed_test_cases
                    - self.incompleteResponses
                    - self.error_test_cases
                )
                + "\n"
            )
            f.write("Total failed testcases : " + str(self.failed_test_cases) + "\n")
            f.write("Total error testcases : " + str(self.error_test_cases) + "\n")
            f.write(
                "Incomplete Responses are : " + str(self.incompleteResponses) + "\n"
            )
            f.write("Tests to repeat : " + str(self.testsToRepeat) + "\n")

        print("Incomplete Responses are ", self.incompleteResponses)
