"""
Module : main
The main pipeline resides here
"""
import ast
from operatorsX import *
import SearchBasedBugFixing.utilsX as utils
import random
from typing import List, Set, Dict, Callable
# from runCode import runCode
import SearchBasedBugFixing.faultLocalizationUtilities as faultLocalizationUtilities
from SearchBasedBugFixing.identifier.identifierVisitorX import IdentifierVisitor
import SearchBasedBugFixing.InsertVisitorX as InsertVisitor
import SearchBasedBugFixing.SwapVisitorX as SwapVisitor

####################################################################
import sys
from io import StringIO
import signal
import sys
# import time


def handler(signum, frame):
    # print('Signal handler called with signal', signum)
    raise Exception("Infinite loop may occured!")

signal.signal(signal.SIGALRM, handler)

def runCode(code: str, myglobals):
    # save the old stdout that is reserved
    oldStdOUT = sys.stdout
    # get the redirected output instance
    redirectedOutput = sys.stdout = StringIO()
    oldStdERR = sys.stderr
    # redirectedOutput2 = sys.stderr = StringIO()
    # result is initially empty
    result = ""
    # there is error
    isError = False
    if (myglobals.get('res')):
        del myglobals['res']
    # start = time.time()
    try:
        # thread.start()
        signal.setitimer(signal.ITIMER_REAL, 0.05)
        exec(code, myglobals)
        signal.setitimer(signal.ITIMER_REAL, 0)
        result = redirectedOutput.getvalue()
    except Exception as e:
        signal.setitimer(signal.ITIMER_REAL, 0)
        isError = True
        result = repr(e)
        if (myglobals.get('testcase')):
            del myglobals['testcase']
        sys.stdout = oldStdOUT
        sys.stderr = oldStdERR
        return result, isError

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
                try:
                    res, isError = runCode(editedProgram, globals())
                except:
                    pass
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
                try:
                    res, isError = runCode(editedProgram, globals())
                except:
                    pass
                res = res.strip()
                # this mutation is of no avail and caused error
                if (isError):
                    return 0
                if (compare_input_output(eval(res), outputs[i])):
                    passedTests += 1
        except Exception as e:
            # print(res)
            # print(editedProgram)
            # print(e)
            return 0
    # print(eval(res))
    # if (eval(res) is None and passedTests == 0):
    #     passedTests = 0
    return passedTests



    
# @profile
def passesNegTests(program:str, program_name:str, inputs:List, outputs:List) -> bool:
    """
    Inputs:
    program : str :  program to be tested
    inputs : List :  inputs to the program
    outputs : List :  outputs of the program
    """
    # let's try by capturing the name of the function in regex and the list of names is compared with the name of the function
    editedProgram = ""
    res = None

    for i in range(len(inputs)):
        try:
            testcase = inputs[i]
            if (len(testcase) == 1):
                testcase = testcase[0]
                if (isinstance(testcase, str)  and testcase.lower() == 'void'):
                    editedProgram = program + f'\n\nres = {program_name}()\n\nprint(res)'
                else:
                    editedProgram = program + f'\n\ntestcase = {testcase}\nres = {program_name}(testcase)\n\nprint(res)'
                
                res, isError = runCode(editedProgram, globals())
                if (isError):
                    return False
                # res = res.strip()

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
                # print(res)
                if (isError):
                    return False
                res = res.strip()
                if (not compare_input_output(eval(res), outputs[i])):
                    return False
        except Exception as e:
            return False
        except:
            return False
    return True



appliedMutations = set()
def update(cand, faultyLineLocations, weightsFaultyLineLocations, ops, name_to_operator, pool, limitLocations = 2):
    # instance of the copy class to be used for copying ASTs
    copier = copyMutation()
    # split the candidate into lines to be able to segment them into tokens and we are working line-wise fault location
    splitted_cand = cand.split('\n')

    # the maximum possible length of faulty locations are the length of the code itself
    limitKPossible = len(faultyLineLocations)
    locationsExtracted = limitKPossible  if (limitKPossible < limitLocations) else limitLocations
    # choose from the locations based on a parameter sent by the user which sould not exceed max length, that is why a limit cap is present
    locs = random.choices(faultyLineLocations, weights = weightsFaultyLineLocations, k=locationsExtracted)

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
    utils.parentify(cand_ast)
    # get the list of identifiers of an ast using IdentifierVisitor
    idVistitor = IdentifierVisitor()
    idVistitor.visit(cand_ast)
    id = idVistitor.get_identifiers()
    func = idVistitor.get_function_identifiers()
    idOcc = idVistitor.get_identifiers_occurences()
    fOcc = idVistitor.get_function_identifiers_occurences()
    # baseOperator.set_identifiers(id)
    # baseOperator.functionArgumentsIdentifiers = f
    # baseOperator.set_functionIdentifiers(f)
    # print(baseOperator.functionArgumentsIdentifiers)
    # print(baseOperator.get_functionIdentifiers())
    for f in locs:
        # parentify the candidate so it will be used by functions like mutate_DIV, mutate_ADD, etc.
        numberSearching = 0 
        try:
            # segment line into presumably tokens
            tokenSet, units_ColOffset = utils.segmentLine(splitted_cand[f - 1])
        except:
            # because the line may be removed by mutations
            continue
        # getting the mutations that can be applied, original tokens and weight of each mutation
        op_f_list, op_f_weights, original_op = ops(tokenSet)
        # op_f_list may be empty as the lines are removed and added, etc. However, running the fault localization again will solve the issue
        if f in fOcc.keys():
            op_f_list.append("FAR")
            op_f_weights.append(10)
        if f in idOcc.keys():
            op_f_list.append("IDR")
            op_f_weights.append(2)
        
        if (op_f_list == []):
            continue
        
        # copy the candidate as not to make the mutation affect the original candidate
        copied_cand = copier.visit(cand_ast)
        copied_cand.type_ignores = []
        utils.parentify(copied_cand)
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
                while ((op_f, f, col_index) in appliedMutations and numberSearching < 2):
                    col_index = random.randint(0, fOcc.get(f))
                    numberSearching += 1
            else:
                col_index = random.randint(0, idOcc.get(f))
                while ((choice, f , col_index) in appliedMutations and numberSearching < 2):
                    col_index = random.randint(0, idOcc.get(f))
                    numberSearching += 1
            appliedMutations.add((choice, f , col_index))
            operation = operator(target_node_lineno = f, indexMutation = col_index, code_ast = copied_cand)
            operation.set_functionIdentifiers(func)
            operation.set_identifiers(id)
            cand_dash = operation.visitC()

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
        # print(op_f)
        cand_dash.type_ignores = []
        ast.fix_missing_locations(cand_dash)
        # if (op_f == "FAR"):
        #     print(ast.dump(cand_dash, indent=4))
        pool.append(cand_dash)
        # return cand to its original ast (despite different location in memory)
        # cand = copied_cand
    return True


def insert(cand:str, pool:set):  # helper function to mutate the code
    # insert will be updated once more to add in certain locations
    # parse the candidate
    try:
        cand_ast = ast.parse(cand)
    except:
        return
    # add type ignores
    cand_ast.type_ignores = []
    # call the function that will insert the node and this function is present in the library insert visitor
    isOk = InsertVisitor.insertNode(cand_ast)
    # add to the possible candidates
    if (isOk):
        cand_ast.type_ignores = []
        # add the line numbers
        try:
            ast.fix_missing_locations(cand_ast)
        except RecursionError as e:
        # print(f"Maximum recursion depth reached: {n}")
            return
        pool.append(cand_ast)
    return

def swap(cand:str, pool:set):  # helper function to mutate the code
    try:
        cand_ast = ast.parse(cand)
        cand_ast.type_ignores = []
    except:
        return
    noError = SwapVisitor.swapNodes(cand_ast)
    if (noError):
        pool.append(cand_ast)
        cand_ast.type_ignores = []
        ast.fix_missing_locations(cand_ast)
    return


def mutate(cand:str, ops:Callable, name_to_operator:Dict, faultyLineLocations: List,
           weightsFaultyLineLocations:List, L:int,  methodUnderTestName:str, inputs:list, outputs:list ):  # helper function to mutate the code

    pool = list()
    availableChoices = {"1": "Insertion", "2": "Swap", "3": "Update"}
    weightsMutation = [0.01, 0.01, 0.98]
    choiceMutation = random.choices(list(availableChoices.keys()), weights=weightsMutation, k=1)[0]
    if availableChoices[choiceMutation] == "Update":
        update(
            cand=cand,
            faultyLineLocations=faultyLineLocations,
            weightsFaultyLineLocations=weightsFaultyLineLocations,
            ops=ops,
            name_to_operator=name_to_operator,
            pool=pool,
            limitLocations=L
        )
        # insert(cand=cand, pool=pool)
    elif availableChoices[choiceMutation] == "Insertion":
        insert(cand=cand, pool=pool)
    elif availableChoices[choiceMutation] == "Swap":
        # print('swap')
        swap(cand=cand, pool=pool)
    
    if (len(pool) == 0):
        return cand

    return pool
    # scores = [] # list of scores that will be used to choose the candidate to be selected
    # poolMod = []
    # for candpool in pool:
    #     try:
    #         parsedCand = ast.unparse(candpool)
    #         # print('pool')
    #         poolMod.append(candpool)
    #         scores.append(fitness_testCasesPassed(parsedCand, methodUnderTestName, inputs, outputs) * 10 + 1) # why +10, just to make it non-zero and also relatively, it stays the same.
    #     except:
    #         pass
    # if (poolMod == []):
    #     return cand
    # choice = random.choices(range(len(poolMod)), weights = scores, k=1)[0]
    # return ast.unparse(poolMod[choice])




def main(BugProgram:str, 
        MethodUnderTestName:str, 
        FaultLocations:List,
        weightsFaultyLocations:List,
        inputs:List, 
        outputs:List,
        FixPar:Callable,
        ops:Callable,
        popSize:int = 3000, 
        M:int = 1,
        E:int = 400, 
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
    storedBugProgram = "".join((c for c in BugProgram)) 
    Solutions = set() # set of solutions
    # passesTests = [0] * popSize
    Pop = []  # population
    for i in range(E):  # E number must be less than or equal to the population size
        Pop.append(BugProgram)  # seeding the population with candidates that were not exposed to mutation
    
    name_to_operator = utils.getNameToOperatorMap()
    while len(Pop) < popSize:
        mutationCandidates = mutate(BugProgram, ops, name_to_operator, FaultLocations, weightsFaultyLocations, L, MethodUnderTestName, inputs, outputs)
        # if not errorOccured:
        scores = [] # list of scores that will be used to choose the candidate to be selected
        poolMod = []
        for candpool in mutationCandidates:
            # try:
            if (type(candpool) is not str):
                # print(type(candpool))
                parsedCand = ast.unparse(candpool)
            else: 
                parsedCand = candpool
            poolMod.append(parsedCand)
            scores.append(fitness_testCasesPassed(parsedCand, MethodUnderTestName, inputs, outputs) * 10 + 1) # why +10, just to make it non-zero and also relatively, it stays the same.
            # except:
            #     pass
        if (poolMod == []):
            Pop.append(BugProgram)
        else:
            choice = random.choices(range(len(poolMod)), weights = scores, k=1)[0]
            Pop.append((poolMod[choice]))  # mutate the population

    # print(len(Pop))
    number_of_iterations = 0
    mutationCandidates = []
    
    while len(Solutions) < M and number_of_iterations < 4:
        # print(number_of_iterations)
        for p_index, p in enumerate(Pop):
            # print(p_index)
            # if not passesTests[p_index]:
            #     mutationCandidate = mutate(p, ops, name_to_operator, FaultLocations, weightsFaultyLocations, L, MethodUnderTestName, inputs, outputs)
            #     if passesNegTests(mutationCandidate, MethodUnderTestName, inputs, outputs):
            #         Solutions.add(mutationCandidate)
            #         passesTests[p_index] = 1
            #     else:
            #         Pop[p_index] = mutationCandidate
            # print(p)
            if p not in Solutions:
                if passesNegTests(p, MethodUnderTestName, inputs, outputs):
                    Solutions.add(p)
                else:
                    res = mutate(p, ops, name_to_operator, FaultLocations, weightsFaultyLocations, L, MethodUnderTestName, inputs, outputs)
                    if (isinstance(res,list)):
                        mutationCandidates.extend(res)
                    else:
                        mutationCandidates.append(res)
                    
                    if (p_index % 10 == 9):
                        scores = [] # list of scores that will be used to choose the candidate to be selected
                        poolMod = []
                        for candpool in mutationCandidates:
                            try:
                                if (type(candpool) is not str):
                                    parsedCand = ast.unparse(candpool)
                                else: parsedCand = candpool
                                poolMod.append(parsedCand)
                                # print('99')
                                scores.append(fitness_testCasesPassed(parsedCand, MethodUnderTestName, inputs, outputs) * 10 + 1) # why +10, just to make it non-zero and also relatively, it stays the same.
                                # print('100')
                            except Exception as e:
                                pass
                        numberMutate = 10
                        if (len(poolMod) < 10):
                            numberMutate = len(poolMod)
                        choice = random.choices(range(len(poolMod)), weights = scores, k=numberMutate)
                        addedindex = 0
                        for i in range(0, numberMutate):
                            if Pop[p_index - i - addedindex] in Solutions:
                                addedindex += 1
                            Pop[p_index - (i+addedindex)] = (poolMod[choice[i]])
                        
                        mutationCandidates = []
                    
        number_of_iterations += 1
        # print('------------------------------------------------------------------------------')
        # print(number_of_iterations)
    return Solutions, Pop




def bugFix(buggyProgram, methodUnderTestName, inputs, outputs):
    buggyProgram = "".join([s for s in buggyProgram.splitlines(True) if s.strip("\r\n")])
    ops = utils.mutationsCanBeApplied # ALIAS to operations that can be applied 
    destinationLocalizationPath = 'SearchBasedBugFixing/testcases/GeneratedTests'
    inputs = ast.literal_eval(inputs)
    outputs = ast.literal_eval(outputs)
    # print(inputs)
    # print(outputs)
    try:
        ast.parse(buggyProgram)
    except:
        print('Syntax Error in the code')
        return 0
    
    # pr = """def kth(arr, k):
    # pivot = arr[0]
    # below = [x for x in arr if x < pivot]
    # above = [x for x in arr if x > pivot]

    # num_less = len(below)
    # num_lessoreq = len(arr) - len(above)

    # if k < num_less:
    #     return kth(below, k)
    # elif k >= num_lessoreq:
    #     return kth(above, k - num_lessoreq)
    # else:
    #     return pivot"""
    # x = passesNegTests(pr, 'kth', inputs, outputs)
    # print(x)
    
    
    # return
    
    error = faultLocalizationUtilities.main(
        code=buggyProgram,
        inputs = inputs, 
        outputs = outputs, 
        function_name= methodUnderTestName, 
        destination_folder= destinationLocalizationPath)
    
    # print('returned from fault localization\n')
    if (error == 0): # 0 means no error
        faultLocations, weightsFaultyLocations = faultLocalizationUtilities.getFaultyLines('..') # fauly locations are in the parent directory
        destination_folder = destinationLocalizationPath
        test_path = f'{destination_folder}/test.py'
        src_path = f'{destination_folder}/source_code.py'
        # s = faultLocalizationUtils.runFaultLocalization(test_path, src_path)
        faultLocations = list(map(int, faultLocations))
        weightsFaultyLocations = list(map(float, weightsFaultyLocations))
        # print(faultLocations)
        # print(weightsFaultyLocations)
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
        print(population[i + 100])
        i += 1
        if (i == 10):
            break
    

    return '\n'.join(list(solutions))
