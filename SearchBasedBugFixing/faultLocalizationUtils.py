import os
import shutil
import ast
import subprocess
from subprocess import TimeoutExpired
import psutil

def kill(proc_pid):
    if psutil.pid_exists(proc_pid):
        process = psutil.Process(proc_pid)
        for proc in process.children(recursive=True):
            if psutil.pid_exists(proc.pid):
                proc.kill()
        process.kill()


def getFaultyLines(folder_path):
    import csv
    # folder_path = 'O:/DriveFiles/GP_Projects/Bug-Repair/Q-A/'

    # filename = 'O:\DriveFiles\GP_Projects\Bug-Repair\FauxPyReport_Q-A_sbfl_statement_2024_04_28_22_54_49_084332\Scores_Tarantula.csv'
    # Get a list of all folders in the directory
    folders = [f for f in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, f))]

    # Find the folder that starts with 'FauxPy'
    fauxpy_folder = next((f for f in folders if f.startswith('FauxPy')), None)
    lines = []
    scores = []

    with open(f'../{fauxpy_folder}/Scores_Tarantula.csv', 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row
        for row in reader:
            if len(row) >= 2:
                # get only the line number 
                lineno = row[0].split('::')[1]
                lines.append(lineno)
                scores.append(row[1])

    # print(lines)
    # print(scores)
    return lines, scores


def deleteFolder(folder_path):
    # Get a list of all folders in the directory
    folders = [f for f in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, f))]

    # Find the folder that starts with 'FauxPy'
    fauxpy_folder = next((f for f in folders if f.startswith('FauxPy')), None)

    # Delete the folder if it exists
    if fauxpy_folder:
        shutil.rmtree(os.path.join(folder_path, fauxpy_folder))
        print(f"The folder '{fauxpy_folder}' has been deleted.")
    else:
        print("No folder starting with 'FauxPy' found.")


def copyFolder(source_folder, destination_folder, file_id):
    # file_id = 1
    # source_folder = f'O:\DriveFiles\GP_Projects\Bug-Repair\Q-A\MyMutpy/testcases\BuggyPrograms'
    # destination_folder = f'{directory_path}'
    file_name = f'{file_id}.txt'

    # Construct the source and destination file paths
    source_file_path = f'{source_folder}/{file_name}'
    destination_file_path = f'{destination_folder}/source_code.py'

    # Copy the file from the source folder to the destination folder
    shutil.copy(source_file_path, destination_file_path)

    print(f"File '{file_name}' copied from '{source_folder}' to '{destination_folder}'.")


def get_value(test_item, hint):
    """
    get_value: sent to it either the input or the output along with its hints
    determine the value based on the hints and return it
    Args:
        inputHints: the hints of the input
        outputHints: the hints of the output
    Returns:
        the value of the input or output
    """
    value = None
    if hint == "int":
        value = int(test_item)
    elif hint == "float":
        value = float(test_item)
    elif hint == "str":
        value = str(test_item)
    elif hint == "bool":
        value = bool(test_item)
    elif hint == "list":
        value = list(test_item)
    elif hint == "tuple":
        value = tuple(test_item)
    elif hint == "set":
        value = set(test_item)
    elif hint == "dict":
        value = dict(test_item)
    elif hint == "None":
        value = None
    return value

def create_py_test(inputs, outputs, function_name, destination_folder):
    pytest_file = ""

    module_ast = ast.parse(pytest_file)
    import_str = "from source_code import *"
    import_node = ast.parse(import_str).body[0]

    # Add the import statement to the beginning of the AST
    module_ast.body.insert(0, import_node)

    # inputs = [[1, 2], [3, 4], [5, 6]]
    # outputs = [3, 7, 11]
    # function_name = "add"
    # function ast
    hintIndex = 0
    for i in range(len(inputs)):
        # definitions of the variables
        val_outputs = []
        val_inputs = []
        assert_str = f"assert "
        fn = f"""def test_{i}(): pass"""

        fn_ast = ast.parse(fn).body[0]
        for j in range(len(inputs[i])):
            # print(inputs[i][j])
            # print('-----------------------------------')
            val_input = (inputs[i][j])
            if (isinstance(val_input, str)):
                val_input = "\'" + val_input + "\'"
            if val_input == "void":
                break
            input_str = f"input_{j} = "
            val_inputs.append(f"input_{j}")
            
            input_str += f"{val_input}"
            input_node = ast.parse(input_str).body[0]
            fn_ast.body.append(input_node)
        
        for j in range(len(outputs[i])):
            # val_output = get_value(outputs[i][j], outputHints[j])
            val_output = (outputs[i][j])
            val_outputs.append(val_output)

        final_output = ""
        # val outputs is the current output string
        if len(val_outputs) == 1:
            if (isinstance(val_outputs[0], str)):
                final_output = "\'" + val_outputs[0] + "\'"
            else:
                final_output = str(val_outputs[0])
        else:
            final_output = str(tuple(val_outputs))
        
        final_input = ""
        for v in val_inputs:
            final_input += v + ", "
        
        if (val_input is None):
            assert_str += f"{function_name}() == {final_output}"
        else:
            assert_str += f"{function_name}({final_input}) == {final_output}"
        assert_node = ast.parse(assert_str).body[0]

        fn_ast.body.append(assert_node)
        # print(ast.unparse(module_ast))
        module_ast.body.append(fn_ast)
    # Check if the destination folder exists
    if not os.path.exists(destination_folder):
        # Create the destination folder if it doesn't exist
        os.makedirs(destination_folder)
        print(f"The folder '{destination_folder}' has been created.")

    # Create the file within the destination folder
    file_path = os.path.join(destination_folder, "test.py")
    with open(file_path, "w") as file:
        # Convert the string to Python code
        python_code = ast.unparse(module_ast)
        file.write(python_code)

        print(f"File 'test.py' created in '{destination_folder}' with the converted Python code.")
    # print(ast.unparse(module_ast))
    # print(ast.dump(module_ast, indent=4))
def runFaultLocalization(test_path, src_path):
    p = subprocess.Popen(["python3", "-m", "pytest", f"{test_path}", "--src", f"{src_path}", "--family", "sbfl", "--granularity", "statement", "--top-n" , "25"], stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    try:
        outs, errs = p.communicate(timeout=3)
    except TimeoutExpired:
        kill(p.pid)
        return -1; # means there is error incurred
    return 0 # means no error


def main(inputs, outputs, function_name, source_folder, destination_folder, file_id, inputHints, outputHints):
    # delete the folder of the fault localization if found
    folder_path = '..'
    deleteFolder(folder_path)

    # Copy the file from the source folder to the destination folder
    copyFolder(source_folder, destination_folder, file_id)

    # Create the PyTest file with the test cases
    create_py_test(inputs, outputs, function_name, destination_folder)

    # Run the fault localization tool
    test_path = f'{destination_folder}/test.py'
    src_path = f'{destination_folder}/source_code.py'
    error = runFaultLocalization(test_path, src_path)
    return error
