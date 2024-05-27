import ast

class IdentifierVisitor(ast.NodeVisitor):
    def __init__(self):
        # self.assignmentIdentifiers = set()
        # self.unknownIdentifiers = set()
        # self.unknownIdentifiersOccurences = dict()
        self.functionIdentifiers = list()
        self.identifiers = list()
        self.identifiersOccurences = dict()
        self.functionIdentifiersOccurences = dict()

    def visit_Name(self, node):
        # print(node.lineno)
        if (isinstance(node.parent, ast.Call) and node is not node.parent.func) or (isinstance(node.parent, ast.Tuple) and hasattr(node.parent, 'dims')):
            self.functionIdentifiers.append(node.id)
            if self.functionIdentifiersOccurences.get(node.lineno) is None:
                self.functionIdentifiersOccurences[node.lineno] = 0
            else:
                self.functionIdentifiersOccurences[node.lineno] += 1
            #######################################################
            self.identifiers.append(node.id)
            if self.identifiersOccurences.get(node.lineno) is None:
                self.identifiersOccurences[node.lineno] = 0
            else:
                self.identifiersOccurences[node.lineno] += 1
        else:
            if (isinstance(node.parent, ast.Call) or isinstance(node.parent, ast.FunctionDef) or isinstance(node.parent, ast.Subscript)):
                return node
            
            self.identifiers.append(node.id)
            if self.identifiersOccurences.get(node.lineno) is None:
                self.identifiersOccurences[node.lineno] = 0
            else:
                self.identifiersOccurences[node.lineno] += 1
        return node

    def get_identifiers(self):
        return self.identifiers

    def get_function_identifiers(self):
        return self.functionIdentifiers
    
    def get_identifiers_occurences(self):
        return self.identifiersOccurences
    
    def get_function_identifiers_occurences(self):
        return self.functionIdentifiersOccurences

