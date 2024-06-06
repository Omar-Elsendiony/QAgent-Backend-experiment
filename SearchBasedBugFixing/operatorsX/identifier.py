import ast
from .base import baseOperator
from typing import Any
import random

class FunctionArgumentReplacement(baseOperator):
    def visit_Call(self, node):
        if (self.wanted_line(node.lineno, 'FAR')):
            if len(node.args) == 1:
                num = random.randint(0, 2)
                if (num == 1):
                    return node.args[0]
            elif len(node.args) == 2:
                num = random.randint(0, 2)
                if (num == 1):
                    node.args[0] , node.args[1] = node.args[1], node.args[0]
        node.func = self.visit(node.func)
        node.args = [self.visit(arg) for arg in node.args]
        node.keywords = [self.visit(kw) for kw in node.keywords]
        return node
        
    def visit_Name(self, node):

        if (node.id in self.get_functionIdentifiers()):
            if (self.wanted_line(node.lineno)):
                # print(node.parent)
                # print(node.parent.func)
                if (node.parent.__class__.__name__ == "Call" and hasattr(node.parent, "func") and hasattr(node.parent.func, "id") and node.parent.func.id != node.id) or node.parent.__class__.__name__ == "Tuple":
                    self.finishedMutation = True
                    op = random.choice([ast.Sub(), ast.Add()])
                    rightIdentifier = random.choice(self.identifiers)
                    right = random.choices([ast.Constant(value=1), ast.Name(id=rightIdentifier, ctx=ast.Load())], weights=[3, 1], k = 1)[0]
                    return ast.BinOp(left=node, op=op, right=right)
        return node
    
    # def visit(self, node):
    #     """Visit a node."""
    #     # if isinstance(node, list): node = node[0] # as it will be a list with first element only
    #     method = 'visit_' + node.__class__.__name__
    #     print(node.__class__.__name__)
    #     visitor = getattr(self, method, self.generic_visit)
    #     if (visitor != self.generic_visit and not self.finishedMutation): # this means that the mutation has already been done
    #         return visitor(node)
    #     if (self.finishedMutation): # this means that the mutation has already been done
    #         return node
    #     return visitor(node)
    
    @classmethod
    def name(cls):
        return 'FAR'  # Function Argument Replacement


class IdentifierReplacement(baseOperator):

    def visit_Name(self, node):
        id = self.get_identifiers()
        if node.id in id:
            if self.wanted_line(node.lineno):
                    # self.mutatedSet.add(node)
                    selectedIdentifier = random.choice(self.identifiers)
                    numRepeat = 0
                    # print(node.id)
                    while(selectedIdentifier == node.id and len(self.identifiers) > 1 and numRepeat < 2):
                        selectedIdentifier = random.choice(self.identifiers)
                        numRepeat += 1
                    node.id = selectedIdentifier
                    # print(node.id)
                    self.finishedMutation = True
        return node

    @classmethod
    def name(cls):
        return 'IDR'

class EnumerateIdentifierReplacement(baseOperator):
    def visit_Name(self, node):
        if (node.id in self.get_functionIdentifiers()):   
            if (self.wanted_line(node.lineno)):
                if (node.parent.__class__.__name__ == "Call" and node.parent.func.id != node.id and node.parent.func.id == "enumerate"):
                    selectedIdentifier = random.choice(self.identifiers)
                    numRepeat = 0
                    while(selectedIdentifier == node.id and len(self.identifiers) > 1 and numRepeat < 2):
                        selectedIdentifier = random.choice(self.identifiers)
                        numRepeat += 1
                    node.id = selectedIdentifier
        return node

    @classmethod
    def name(cls):
        return 'EIR'