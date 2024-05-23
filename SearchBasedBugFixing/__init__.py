# # import base
# # import ast
# # from operators import *
# # import operators
# # import astunparse



# # def build_name_to_operator_map():
# #     result = {}
# #     for operator in operators.standard_operators | operators.experimental_operators:
# #         result[operator.name()] = operator
# #         # result[operator.long_name()] = operator
# #     return result



# # code = """s = 1 + 2;
# # s = 1 + 2"""
# # ast_node = ast.parse(code)
# # mutant = (ArithmeticOperatorReplacement(target_node_lineno = 1, code = ast_node)).visitC()
# # mutant = ast.fix_missing_locations(mutant) # after mutation, we need to fix the missing locations
# # mutant = (ArithmeticOperatorReplacement(target_node_lineno= 2, code = mutant)).visitC()
# # # print(ast.dump(mutant, indent=4))
# # print(astunparse.to_source(ast_node))


# # # again = ArithmeticOperatorReplacement.printMutatedSet()

# # res = build_name_to_operator_map()

# # print(res)
# import faultLocalizationUtils

# destinationLocalizationPath = 'O:/DriveFiles/GP_Projects/Bug-Repair/Q-A/MyMutpy/testcases/GeneratedTests'
# destination_folder = destinationLocalizationPath


# test_path = f'{destination_folder}/test.py'
# src_path = f'{destination_folder}/source_code.py'
# faultLocalizationUtils.runFaultLocalization(test_path, src_path)





