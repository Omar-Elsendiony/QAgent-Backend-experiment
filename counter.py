import pandas as pd

OldFile = "Results/Mixtral-3Shot/"
OldCasesFile = OldFile + "RunningLogs.jsonl"
OldCasesFile = "humaneval.jsonl"
OldCases = pd.read_json(OldCasesFile, lines=True)
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
        print(OldCases.iloc[i]["text"])
        print(OldCases.iloc[i]["canonical_solution"])
        print(OldCases.iloc[i]["canonical_solution"])
        print(OldCases.iloc[i]["declaration"])
        print("Test case {i}\n===================================\n".format(i=i))
        f.write("Test case {i}\n===================================\n".format(i=i))
        f.write(OldCases.iloc[i]["text"])
        f.write(OldCases.iloc[i]["canonical_solution"])
        f.write(OldCases.iloc[i]["canonical_solution"])
        f.write(OldCases.iloc[i]["declaration"])
        # print(OldCases.iloc[i]["GeneratedCode"])
        # print(OldCases.iloc[i]["Feedback"])
        # f.write(OldCases.iloc[i]["GeneratedCode"])
        # f.write(OldCases.iloc[i]["Feedback"])
        # OlFailTotal += OldCases.iloc[i]["Old Tests Failed"]
        # NowTotal += OldCases.iloc[i]["Feedback Total Tests"]
        # NowFailTotal += OldCases.iloc[i]["Feedback Tests failed"]
    # print(OldCases)
    print("Old Total: ", OlTotal)
    # print("Old Fail Total: ", OlFailTotal)
    # print("Now Total: ", NowTotal)
    # print("Now Fail Total: ", NowFailTotal)
