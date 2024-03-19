import pandas as pd
from utils.FeedbackUtils import *
from utils.LLMUtilis import *

OldFile = "FeedbackOutput/"
OldFile = "Results/FeedbackMixtral-2Shot/"
OldCasesFile = OldFile + "RunningLogs.json"
# OldCasesFile = "humaneval.jsonl"
OldCases = pd.read_json(OldCasesFile, lines=False)
OlTotal = 0
OlFailTotal = 0
NowTotal = 0
NowFailTotal = 0


with open("Heval1.txt", "w") as f:
    for i in range(len(OldCases)):
        # OlTotal += OldCases.iloc[i]["Old Total Tests"]
        # if OldCases.iloc[i]["Feedback Tests failed"] > 0:
        #     OlTotal += OldCases.iloc[i]["Feedback Total Tests"]
        print("Test case {i}\n===================================\n".format(i=i))
        f.write("Test case {i}\n===================================\n".format(i=i))
        print(OldCases.iloc[i]["GeneratedCode"])
        f.write(OldCases.iloc[i]["GeneratedCode"] + "\n=====================\n")
        # print(OldCases.iloc[i]["FullFeedback"])
        # f.write(OldCases.iloc[i]["GeneratedCode"])
        FullFeedback = OldCases.iloc[i]["Feedback"]
        print(FullFeedback, "\n=====================\n")
        f.write(FullFeedback + "\n=====================\n")
        # indices = getFailedTestcasesIndices(FullFeedback)
        # tests = getEachTestCase(OldCases.iloc[i]["GeneratedCode"], indices)
        # print(indices, "\n=====================\n")
        # print(tests, "\n=====================\n")
        # OlFailTotal += OldCases.iloc[i]["Old Tests Failed"]
        testsToRepeat = OldCases.iloc[i]["TestsToRepeat"]
        print(testsToRepeat)
        f.write(testsToRepeat + "\n=====================\n")
        # NowTotal += OldCases.iloc[i]["Feedback Total Tests"]
        # NowFailTotal += OldCases.iloc[i]["Feedback Tests failed"]
    # print(OldCases)
    # print("Old Total: ", OlTotal)
    # print("Old Fail Total: ", OlFailTotal)
    # print("Now Total: ", NowTotal)
    # print("Now Fail Total: ", NowFailTotal)
