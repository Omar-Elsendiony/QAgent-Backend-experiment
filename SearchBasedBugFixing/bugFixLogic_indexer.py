"""
Module : main
The main pipeline resides here
"""
import ast
import re
from operatorsX import *
import utilsX
import random
from typing import List, Set, Dict, Callable
# from runCode import runCode
import faultLocalizationUtils
from identifier.identifierVisitorX import IdentifierVisitor
import InsertVisitorX
import SwapVisitorX

####################################################################
import sys
from io import StringIO
import signal
###################################################################
import numpy as np
import faiss

index = faiss.read_index('../../flatIP_index_all.index')
import torch
from unixcoder import UniXcoder
import numpy as np
DEVICE = torch.device("cuda")
model = UniXcoder("microsoft/unixcoder-base")
model.to(DEVICE)

#returns numpy array of embeddings
# def get_embeddings(model,tokens,device=DEVICE):
#   tokens_ids = model.tokenize([tokens],max_length=512,mode="<encoder-only>")
#   source_ids = torch.tensor(tokens_ids).to(device)
#   _,embeddings = model(source_ids)
#   return embeddings.detach()

from torch.utils.data import DataLoader

def batch_tokenize(token_list, max_length=512, mode="<encoder-only>"):
    # Tokenize multiple tokens in batches
    token_ids = model.tokenize(token_list, max_length=max_length, mode=mode)
    
    # Ensure token_ids are converted to a tensor and moved to GPU
    return torch.tensor(token_ids).to(DEVICE)

def fitness_bug_code(tokens,device=DEVICE):
  tokens_ids = model.tokenize([tokens],max_length=512,mode="<encoder-only>")
  source_ids = torch.tensor(tokens_ids).to(device)
  _ , embeddings = model(source_ids)
  normEmb =  torch.nn.functional.normalize(embeddings, dim=1)
  n = normEmb.detach().cpu()
  D, I = index.search(n, k=1)
  
  # print(D[0][0])

  return D[0][0]



def handler(signum, frame):
    # print('Signal handler called with signal', signum)
    raise Exception("Infinite loop may occured!")

def runCode(code: str, myglobals):
    # save the old stdout that is reserved
    oldStdOUT = sys.stdout
    # get the redirected output instance
    redirectedOutput = sys.stdout = StringIO()
    oldStdERR = sys.stderr
    redirectedOutput2 = sys.stderr = StringIO()
    # result is initially empty
    result = ""
    # there is error
    isError = False
    if (myglobals.get('res')):
        del myglobals['res']
    try:
        # thread.start()
        signal.signal(signal.SIGALRM, handler)
        signal.setitimer(signal.ITIMER_REAL, 0.05)
        exec(code, myglobals)
        # signal.alarm(0)
        signal.setitimer(signal.ITIMER_REAL, 0)

        result = redirectedOutput.getvalue()
    except Exception as e:
        signal.setitimer(signal.ITIMER_REAL, 0)
        isError = True
        result = repr(e)
    # except SystemExit as s:
    #     isError = True
    #     result = redirectedOutput2.getvalue()
    # except KeyboardInterrupt as k:
    #     isError = True
    #     result = "timed out"
        # print('timey')
    # thread.stop()
    # signal.alarm(0)
    if (myglobals.get('testcase')):
        del myglobals['testcase']
    sys.stdout = oldStdOUT
    sys.stderr = oldStdERR

    return result, isError
####################################################################

def editFreq(cand):
    ## TODO ##
    pass

def compare_input_output(res, output):
    outputMod = output
    if (type(output) is list):
        if len(output) == 1:
            outputMod = output[0]
        else:
            outputMod = tuple(output)

    if (res == outputMod):
        return True
    return False


def fitness_testCasesPassed(program:str, program_name:str, inputs:List, outputs:List) -> int:
    """
    Inputs:
    program : str :  program to be tested
    inputs : List :  inputs to the program
    outputs : List :  outputs of the program
    """
    # let's try by capturing the name of the function in regex and the list of names is compared with the name of the function
    editedProgram = None
    res = None
    passedTests = 0

    for i in range(len(inputs)):
        try:
            testcase = inputs[i]
            if (len(testcase) == 1):
                testcase = testcase[0]
                if (isinstance(testcase, str)  and testcase.lower() == 'void'):
                    editedProgram = program + f'\n\nres = {program_name}()\n\nprint(res)'
                else:
                    editedProgram = program + f'\n\ntestcase = {testcase}\nres = {program_name}({testcase})\n\nprint(res)'
                res, isError = runCode(editedProgram, globals())
                if (isError):
                    return 0
                res = res.strip()
                if (compare_input_output(eval(res), outputs[i])):
                    passedTests += 1
            else:
                inputStrings = ""
                outputStrings = ""
                for argIndex, arg in enumerate(testcase):
                    if isinstance(arg, str):
                        arg = '\"' + arg + '\"'
                    input_inp = f'input_{argIndex} = {arg}\n'
                    inputStrings += input_inp
                for argIndex in range(len(testcase)):
                    output_out = f'input_{argIndex},'
                    outputStrings += output_out
                editedProgram = program + '\n' + inputStrings + f'\nres = {program_name}({outputStrings})\n\nprint(res)'

                res, isError = runCode(editedProgram, globals())
                res = res.strip()
                # this mutation is of no avail and caused error
                if (isError):
                    return 0
                if (compare_input_output(eval(res), outputs[i])):
                    passedTests += 1
        except Exception as e:
            # print(e)
            return 0
    # print(eval(res))
    # if (eval(res) is None and passedTests == 0):
    #     passedTests = 0
    return passedTests

pooolooo = 0

def passesNegTests(program:str, program_name:str, inputs:List, outputs:List) -> bool:
    """
    Inputs:
    program : str :  program to be tested
    inputs : List :  inputs to the program
    outputs : List :  outputs of the program
    """
    # let's try by capturing the name of the function in regex and the list of names is compared with the name of the function
    global pooolooo
    print(pooolooo)
    pooolooo += 1
    editedProgram = ""
    res = None
    for i in range(len(inputs)):
        print(str(i) + "++++++")
        try:
            testcase = inputs[i]
            print(testcase)
            if (len(testcase) == 1):
                testcase = testcase[0]
                if (isinstance(testcase, str)  and testcase.lower() == 'void'):
                    editedProgram = program + f'\n\nres = {program_name}()\n\nprint(res)'
                else:
                    editedProgram = program + f'\n\ntestcase = {testcase}\nres = {program_name}(testcase)\n\nprint(res)'
                res, isError = runCode(editedProgram, globals())
                if (isError):
                    return False
                res = res.strip()
                print(res)
                # print(outputs[0][0])
                if (not compare_input_output(eval(res), outputs[i])):
                    return False
            else:
                inputStrings = ""
                outputStrings = ""
                for argIndex, arg in enumerate(testcase):
                    if isinstance(arg, str):
                        arg = '\"' + arg + '\"'
                    input_inp = f'input_{argIndex} = {arg}\n'
                    inputStrings += input_inp
                for argIndex in range(len(testcase)):
                    output_out = f'input_{argIndex},'
                    outputStrings += output_out
                editedProgram = program + '\n' + inputStrings + f'\nres = {program_name}({outputStrings})\n\nprint(res)'

                res, isError = runCode(editedProgram, globals())
                print(res)
                print(i)
                print('***********************')
                print(outputs[i])
                print('***********************')

                if (isError):
                    return False
                res = res.strip()
                if (not compare_input_output(eval(res), outputs[i])):
                    return False
        except Exception as e:
            return False
    # print(eval(res))
    return True


# import subprocess
# def passesNegTests_2(program:str, program_name:str, inputs:List, outputs:List):
#     test_path = f'testcases/GeneratedTests/test.py'
#     src_path = f'testcases/GeneratedTests/source_code.py'
#     res = subprocess.run(["python3", "-m", "pytest", f"{test_path}"], stderr=subprocess.PIPE, stdout=subprocess.PIPE)
#     # print(str(res).split()[-1])
#     res = res.stdout.decode('utf-8')
#     splitted = res.split()
#     passed = None; Failed = None
#     passOrFailedNum = splitted[-5]
#     passOrFailedString = splitted[-4]
#     if (passOrFailedString == "passed"):
#         passed = passOrFailedNum
#     else:
#         Failed = passOrFailedNum
#         passed = 0
#     if passed == len(inputs):
#         return True
#     else:
#         return False

# def passesNegTests_3(program:str, program_name:str, inputs:List, outputs:List):
#     test_path = f'testcases/GeneratedTests/test.py'
#     src_path = f'testcases/GeneratedTests/source_code.py'
#     res = subprocess.run(["python3", "-m", "pytest", f"{test_path}"], stderr=subprocess.PIPE, stdout=subprocess.PIPE)
#     # print(str(res).split()[-1])
#     res = res.stdout.decode('utf-8')
#     splitted = res.split()
#     passed = None; Failed = None
#     passOrFailedNum = splitted[-5]
#     passOrFailedString = splitted[-4]
#     if (passOrFailedString == "passed"):
#         passed = passOrFailedNum
#     else:
#         Failed = passOrFailedNum
#         passed = 0
#     return passed



# def selectPool(candidates:List, inputs:List, outputs:List):
#     """Select pool determined by the number of testcases passed by the candidates"""
#     # scores = [] # list of scores that will be used to choose the candidate to be selected
#     # # # print(str(len(candidates))+'---------------------------------------')
#     # for cand in candidates:
#     #     scores.append(passesNegTests_3(ast.unparse(cand), methodUnderTestName, inputs, outputs) + 10) # why +10, just to make it non-zero and also relatively, it stays the same.
#     # choice = random.choices(range(len(candidates)), weights = scores, k=1)[0]

#     return ast.unparse(candidates[0])
#     # return (ast.unparse(candidates[0]))


# def selectPool(candidates:Set) -> Set:
#     pass


appliedMutations = set()
def update(cand, faultyLineLocations, weightsFaultyLineLocations, ops, name_to_operator, pool,
           limitLocations = 2, linesMutated = []):
    # instance of the copy class to be used for copying ASTs
    copier = copyMutation()
    # split the candidate into lines to be able to segment them into tokens and we are working line-wise fault location
    splitted_cand = cand.split('\n')

    # the maximum possible length of faulty locations are the length of the code itself
    limitKPossible = len(faultyLineLocations)
    locationsExtracted = limitKPossible  if (limitKPossible < limitLocations) else limitLocations
    # choose from the locations based on a parameter sent by the user which sould not exceed max length, that is why a limit cap is present
    locs = random.choices(faultyLineLocations, weights = weightsFaultyLineLocations, k=1)

    # candidate that will be mutated
    cand_dash = None
    # parse the candidate
    try:
        cand_ast = ast.parse(cand)
    except:
        return False
    # add this line as type ignores gets missed in the mutations and it is needed in ast.unparse
    cand_ast.type_ignores = []

    # parentify the candidate so it will be used by functions like mutate_DIV, mutate_ADD, etc.
    utilsX.parentify(cand_ast)
    # get the list of identifiers of an ast using IdentifierVisitor
    idVistitor = IdentifierVisitor()
    idVistitor.visit(cand_ast)
    idOcc = idVistitor.get_identifiers_occurences()
    fOcc = idVistitor.get_function_identifiers_occurences()
    id = idVistitor.get_identifiers()
    f = idVistitor.get_function_identifiers()
    baseOperator.set_identifiers(id)
    baseOperator.set_functionIdentifiers(f)

    for f in locs:
        # parentify the candidate so it will be used by functions like mutate_DIV, mutate_ADD, etc.
        numberSearching = 0 
        try:
            # segment line into presumably tokens
            tokenSet, units_ColOffset = utilsX.segmentLine(splitted_cand[f - 1])
        except:
            # because the line may be removed by mutations
            continue
        # getting the mutations that can be applied, original tokens and weight of each mutation
        op_f_list, op_f_weights, original_op = ops(tokenSet)
        # op_f_list may be empty as the lines are removed and added, etc. However, running the fault localization again will solve the issue
        if f in fOcc.keys():
            op_f_list.append("FAR")
            op_f_weights.append(8)
        if f in idOcc.keys():
            op_f_list.append("IDR")
            op_f_weights.append(2)
        if (op_f_list == []):
            continue
        
        # copy the candidate as not to make the mutation affect the original candidate
        copied_cand = copier.visit(cand_ast)
        copied_cand.type_ignores = []
        utilsX.parentify(copied_cand)
        # changed from choosing the actual element to choosing the index, as getting 
        # the operator attributed to the mutation is not possible with index

        # Choose the index with the higher probability
        choice_index = random.choices(range(len(op_f_list)), weights = op_f_weights, k=1)[0]
        # Get the operation neumonic from operation list
        op_f = op_f_list[choice_index] #op_f is the choice selected from list of plausible operations
        while (op_f != "FAR" and op_f != "IDR" and (op_f, f) in appliedMutations and numberSearching < 2):
            choice_index = random.choices(range(len(op_f_list)), weights = op_f_weights, k=1)[0]
            op_f = op_f_list[choice_index]
            numberSearching += 1
        
        if (op_f == "FAR" or op_f == "IDR"):
            operator = name_to_operator[op_f]
            if (op_f == "FAR"):
                col_index = random.randint(0, fOcc.get(f))
                if f == 11:
                    # print(col_index)
                    col_index = 2
                while ((op_f, f, col_index) in appliedMutations and numberSearching < 2):
                    col_index = random.randint(0, fOcc.get(f))
                    numberSearching += 1
            else:
                col_index = random.randint(0, idOcc.get(f))
                while ((choice, f , col_index) in appliedMutations and numberSearching < 2):
                    col_index = random.randint(0, idOcc.get(f))
                    numberSearching += 1
            appliedMutations.add((choice, f , col_index))
            cand_dash = operator(target_node_lineno = f, indexMutation = col_index, code_ast = copied_cand).visitC()

        else:
            appliedMutations.add((op_f, f))
            # get the colum offset occurances of such an operation
            colOffsets = units_ColOffset[original_op[choice_index]]
            # get an index of the operation that you want to apply on
            col_index = random.randint(0, len(colOffsets) - 1)
            # get the operator class that holds all the logic from the 3 letters neumonic
            operator = name_to_operator[op_f]
            col_index = col_index if op_f != "ARD" else choice_index // 2
            # apply the mutation and acquire a new candidate
            cand_dash = operator(target_node_lineno = f, code_ast = copied_cand, indexMutation= col_index, specifiedOperator=original_op[choice_index]).visitC() # f + 1 because the line number starts from 1

        # adds/corrects the line number as well as column offset
        ast.fix_missing_locations(cand_dash)
        cand_dash.type_ignores = []
        # add the candidate to the pool that you will select from
        try:
            ast.unparse(cand_dash)
            pool.append(cand_dash)
            linesMutated.append(splitted_cand[f - 1])
        except:
            pass
    return True


def insert(cand:str, pool:set):  # helper function to mutate the code
    # insert will be updated once more to add in certain locations
    # parse the candidate
    cand_ast = ast.parse(cand)
    # add type ignores
    cand_ast.type_ignores = []
    # call the function that will insert the node and this function is present in the library insert visitor
    isOk = InsertVisitorX.insertNode(cand_ast)
    # add to the possible candidates
    if (isOk):
        pool.append(cand_ast)
        cand_ast.type_ignores = []
        # add the line numbers
        ast.fix_missing_locations(cand_ast)
    return

def swap(cand:str, pool:set):  # helper function to mutate the code
    try:
        cand_ast = ast.parse(cand)
        cand_ast.type_ignores = []
    except:
        return
    noError = SwapVisitorX.swapNodes(cand_ast)
    if (noError):
        pool.append(cand_ast)
        cand_ast.type_ignores = []
        ast.fix_missing_locations(cand_ast)
    return


def mutate(cand:str, ops:Callable, name_to_operator:Dict, faultyLineLocations: List,
           weightsFaultyLineLocations:List, L:int,  methodUnderTestName:str, inputs:list, outputs:list ):  # helper function to mutate the code

    pool = list()
    linesMutated = list()
    availableChoices = {"1": "Insertion", "2": "Swap", "3": "Update"}
    weightsMutation = [0.01, 0.01, 0.98]
    choiceMutation = random.choices(list(availableChoices.keys()), weights=weightsMutation, k=1)[0]
    if availableChoices[choiceMutation] == "Update" or availableChoices[choiceMutation] == "Insertion":
        update(
            cand=cand,
            faultyLineLocations=faultyLineLocations,
            weightsFaultyLineLocations=weightsFaultyLineLocations,
            ops=ops,
            name_to_operator=name_to_operator,
            pool=pool,
            limitLocations=L,
            linesMutated=linesMutated
        )
        # insert(cand=cand, pool=pool)
    elif availableChoices[choiceMutation] == "Insertion":
        insert(cand=cand, pool=pool)
    elif availableChoices[choiceMutation] == "Swap":
        swap(cand=cand, pool=pool)
    if (len(pool) == 0):
        return cand
    if (len(pool) == 1):
        return ast.unparse(pool[0])
    scores = [] # list of scores that will be used to choose the candidate to be selected
    candI = 0
    for cand in pool:
        # try:
        scores.append(10 * fitness_bug_code(linesMutated[candI]) + 1) # why +10, just to make it non-zero and also relatively, it stays the same.
        # except:
        #     scores.append(0.000000000000001)
        # candI += 1
    choice = random.choices(range(len(pool)), weights = scores, k=1)[0]
    returnedVal = ast.unparse(pool[choice])
    # print(returnedVal)
    return returnedVal



def main(BugProgram:str, 
        MethodUnderTestName:str, 
        FaultLocations:List,
        weightsFaultyLocations:List,
        inputs:List, 
        outputs:List, 
        FixPar:Callable,
        ops:Callable,
        popSize:int = 5900, 
        M:int = 1,
        E:int = 10, 
        L:int = 5):
    """
    Inputs:
    BugProgram : str :  buggy program
    FaultLocations : List : the locations of the fault
    inputs : List :  inputs to the program
    outputs : List :  outputs of the program
    FixPar : Callable : distribution sampled from when comparing with history fix
    ops : Callable : operations that can be applied for the given fault location
    popSize : int :  population size
    M : int :  number of desired solutions that serves as the upper limit
    E : int :  number of seeded candidates to the initial population
    L: int: number of locations considered in the mutation step
    """
    Solutions = set() # set of solutions
    Pop = []  # population
    for i in range(E):  # E number must be less than or equal to the population size
        Pop.append(BugProgram)  # seeding the population with candidates that were not exposed to mutation
    
    name_to_operator = utilsX.getNameToOperatorMap()
    ilo = 0
    while len(Pop) < popSize:
        newMutation= mutate(BugProgram, ops, name_to_operator, FaultLocations, weightsFaultyLocations, L, MethodUnderTestName, inputs, outputs)
        # if not errorOccured:
        # print(ilo)
        ilo += 1
        Pop.append(newMutation)  # mutate the population

    # print(len(Pop))
    number_of_iterations = 0
    while len(Solutions) < M and number_of_iterations < 4:
        print(number_of_iterations)
        for p_index, p in enumerate(Pop):
            if p not in Solutions:
                if passesNegTests(p, MethodUnderTestName, inputs, outputs):
                    Solutions.add(p)
                else:
                    mutationCandidate = mutate(p, ops, name_to_operator, FaultLocations, weightsFaultyLocations, L, MethodUnderTestName, inputs, outputs)
                    Pop[p_index] = mutationCandidate
                    if passesNegTests(mutationCandidate, MethodUnderTestName, inputs, outputs):
                        Solutions.add(mutationCandidate)
                        break
        number_of_iterations += 1
    return Solutions, Pop




def bugFix():
    ops = utilsX.mutationsCanBeApplied # ALIAS to operations that can be applied 
    inputs = []
    outputs = []
    inputProgramPath = 'testcases/BuggyPrograms'
    destinationLocalizationPath = 'testcases/GeneratedTests'
    inputCasesPath = 'testcases/Inputs'
    outputCasesPath = 'testcases/Outputs'
    metaDataPath = 'testcases/MetaData'
    file_id = 9
    file_name = f'{file_id}.txt'
    typeHintsInputs = []
    typeHintsOutputs = []
    methodUnderTestName = None

    try:
        with open(f'{inputProgramPath}/{file_name}', 'r') as file:
            buggyProgram = file.read()
            try:
                bp = ast.parse(buggyProgram)
            except:
                print("Problem in parsing the buggy program")
                exit(-1)
        with open(f'{metaDataPath}/{file_name}', 'r') as file:
            lines = file.readlines()
            methodUnderTestName = lines[0].strip()
            function_names = re.findall(r'def\s+(\w+)', buggyProgram)
            foundName = False
            for name in function_names:
                if name == methodUnderTestName:
                    foundName = True
                    break
            if not foundName:
                print("Function name not found")
                exit(-1)   
            l = 1
            # while(lines[l] != '\n'):
            #     typeHintsInputs.append(lines[l].strip())
            #     # utilsX.processLine(lines[l], l, inputs)
            #     l += 1
            # l += 1
            # while(l < len(lines) and lines[l] != '\n'):
            #     typeHintsOutputs.append(lines[l].strip())
            #     # utilsX.processLine(lines[l], l, inputs)
            #     l += 1
        with open(f'{inputCasesPath}/{file_name}', 'r') as file:
            lines = file.readlines()
            i = 0
            k = 0
            inputTestCase = []
            for line in lines:
                if (line == '\n'):
                    if (inputTestCase != []) : inputs.append(inputTestCase); inputTestCase = []; k = 0
                    else:
                        continue
                else: 
                    utilsX.processLine(line, i, inputTestCase)
                    i += 1; k += 1
            if (inputTestCase != []):
                inputs.append(inputTestCase)

        with open(f'{outputCasesPath}/{file_name}', 'r') as file:
            lines = file.readlines()
            i = 0
            k = 0
            outputTestCase = []
            for line in lines:
                if (line == '\n'):
                    if (outputTestCase != []) : outputs.append(outputTestCase);outputTestCase = [];k = 0
                    else: 
                        continue
                else: 
                    utilsX.processLine(line, i, outputTestCase)
                    i += 1 ; k += 1
            if (outputTestCase != []):
                outputs.append(outputTestCase)
    except Exception as e:
        print("Problem in reading files, insufficient data")
        print(e)
        exit(-1)
    print(inputs)
    print(outputs)

    pr = """def levenshtein(source, target):
    if source == '' or target == '':
        return len(source) or len(target)
    elif source[0] == target[0]:
        return 1 + levenshtein(source[1:], target[1:]) 
    else:
        return 1 + min(
            levenshtein(source,     target[1:]),
            levenshtein(source[1:], target[1:]),
            levenshtein(source[1:], target)
        )"""
    x = passesNegTests(pr, 'levenshtein', inputs, outputs)
    print(x)
    return


    error = faultLocalizationUtils.main(
        inputs = inputs, 
        outputs = outputs, 
        function_name= methodUnderTestName, 
        source_folder= inputProgramPath, 
        destination_folder= destinationLocalizationPath, 
        file_id= file_id,
        inputHints=typeHintsInputs,
        outputHints=typeHintsOutputs)
    print('returned from fault localization\n')
    if (error == 0): # 0 means no error
        faultLocations, weightsFaultyLocations = faultLocalizationUtils.getFaultyLines('..') # fauly locations are in the parent directory
        destination_folder = destinationLocalizationPath
        test_path = f'{destination_folder}/test.py'
        src_path = f'{destination_folder}/source_code.py'
        # s = faultLocalizationUtils.runFaultLocalization(test_path, src_path)
        faultLocations = list(map(int, faultLocations))
        weightsFaultyLocations = list(map(float, weightsFaultyLocations))
    # else:
    if (error != 0 or faultLocations == []):
        splittedBuggyProgram = buggyProgram.split('\n')
        allLines = len(splittedBuggyProgram)
        faultLocations = list(range(1, allLines + 1))
        weightsFaultyLocations = [1] * (allLines)

    solutions, population = main(BugProgram=buggyProgram, 
                    MethodUnderTestName=methodUnderTestName, 
                    FaultLocations=faultLocations, 
                    weightsFaultyLocations=weightsFaultyLocations, 
                    inputs=inputs,
                    outputs=outputs, 
                    FixPar=None,
                    ops=ops)
    print("************************************************************")
    for solution in solutions:
        print(solution)
    print("************************************************************")
    print(len(population))
    i = 0
    for p in population:
        # splt = p.split()
        print(population[i])
        i += 1
        if (i == 10):
            break
    # print(methodUnderTestName)
    # print(buggyProgram)
