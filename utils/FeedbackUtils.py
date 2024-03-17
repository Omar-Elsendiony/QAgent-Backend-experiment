###### This file contains the functions to parse the feedback from running the code and extract the relevant information from it. ######

import re


# gets feedback from running the code using exec
# empty in case of success
def get_feedback_from_run(response):
    lines = response.split("\n")
    feedback = ""
    in_failmessage = False
    if lines[0].startswith("F") or lines[0].startswith(".") or lines[0].startswith("E"):
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


def get_failed_testcases(feedback):
    # Use a regular expression to find the number of Ran Tests and Failures
    failures_match = re.search(r"failures=(\d+)", feedback)
    errors_match = re.search(r"errors=(\d+)", feedback)
    # Extract the numbers or default to 0 if not found
    failures = int(failures_match.group(1)) if failures_match else 0
    errors = int(errors_match.group(1)) if errors_match else 0

    return failures, errors


def getFailedTestcasesIndices(feedback):
    lines = feedback.split("\n")
    indices = []
    firstline = lines[0]
    if (
        firstline.startswith("F")
        or firstline.startswith(".")
        or firstline.startswith("E")
    ):
        for i in range(len(firstline)):
            if firstline[i] == "F" or firstline[i] == "E":
                indices.append(i)
    return indices


def get_num_assertions(code_text):
    total_num = len(re.findall(r"self\.assert", code_text, flags=re.MULTILINE))
    return total_num
