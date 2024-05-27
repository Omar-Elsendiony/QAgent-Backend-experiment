import ast
from .base import baseOperator
from random import choice



class FunctionArgumentReplacement(baseOperator):

    def visit_Name(self, node):
        if not (hasattr(node, 'parent')): return node
        if (node.parent.__class__.__name__ == "Call"):
            # print(node.parent.func.id + "weeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee")
            if (node.parent.func.id == node.id): return node
            return ast.BinOp(left=ast.Name(id=node.id, ctx=ast.Load()), op=ast.Sub(), right=ast.Constant(value=1))
        else:
            return node
    
    @classmethod
    def name(cls):
        return 'FAR'  # Function Argument Replacement
