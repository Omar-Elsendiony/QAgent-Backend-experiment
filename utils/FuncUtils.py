import re

# made according to human eval


def extract_function_name(string):
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
def get_function_name(funcDefiniton):
    rs = re.search(r"\"\"\".*\"\"\"", funcDefiniton, re.DOTALL)
    if rs == None:
        rs = re.search(r"\'\'\'.*\'\'\'", funcDefiniton, re.DOTALL)
    end = rs.span()[0]
    funcDefiniton = funcDefiniton[:end]
    return funcDefiniton


# replace function name if needed
def replace_function_name(string, replacement_string):
    # Define the regular expression pattern to match the function name
    pattern = r"def\s+(\w+)\s*"

    # Use re.sub() to replace the pattern with the replacement string
    modified_string = re.sub(pattern, "def " + replacement_string, string)

    return modified_string
