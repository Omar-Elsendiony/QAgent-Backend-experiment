"""
logical operators: Module meant to mutate logical operators
LTE: less than or equal to
GTE: greater than or equal to
LT: less than
GT: greater than
NE: not equal
EQ: equal
AND: and
OR: or
NOT: not
CR: comparison
MR: membership
"""
import ast
from .base import baseOperator
from random import choice

class LogicalOperator(baseOperator):
    """
    LogicalOperator: Class meant to mutate logical operators
    """
    # def __init__(self, target_node_lineno = None, code_ast = None, target_node_col_offset=None):
    #     super().__init__(target_node_lineno, code_ast, target_node_col_offset)
    
    @classmethod
    def name(cls):
        return 'LO'  # Logical Operator

class RelationalOperatorReplacement(LogicalOperator):
    """
    LogicalOperatorReplacement: Umbrella for all replacements of logical operators
    takes as argument the logical operator to be replaced, checks its type, based on the type of the operator,
    it will mutate based on the applicable operators.
    """
    def get_operator_type(self):
        """
        get_operator_type: Method to get the operator type
        """
        return ast.Lt, ast.Gt, ast.LtE, ast.GtE, ast.Eq, ast.NotEq

    def visit_Compare(self, node):
        """
        Visit a Compare node
        """
        if not (self.wanted_line(node.lineno)):
            return node
        self.finishedMutation = True
        operationChoice = choice([ast.Gt, ast.LtE, ast.GtE, ast.Eq, ast.NotEq])()
        # print(operationChoice)
        if isinstance(node.ops[0], ast.Lt):
            # choice([ast.Gt, ast.LtE, ast.GtE, ast.Eq, ast.NotEq])
            node.ops[0] = operationChoice
        elif isinstance(node.ops[0], ast.Gt):
            node.ops[0] = operationChoice
        elif isinstance(node.ops[0], ast.LtE):
            node.ops[0] = operationChoice
        elif isinstance(node.ops[0], ast.GtE):
            node.ops[0] = operationChoice
        elif isinstance(node.ops[0], ast.Eq):
            node.ops[0] = operationChoice
        elif isinstance(node.ops[0], ast.NotEq):
            node.ops[0] = operationChoice
        elif isinstance(node.ops[0], ast.In):
            node.ops[0] = ast.NotIn()
        elif isinstance(node.ops[0], ast.NotIn):
            node.ops[0] = ast.In()
        
        return node

    @classmethod
    def name(cls):
        return 'ROR'  # Relational Operator Replacement



class LogicalOperatorReplacement(LogicalOperator):
    def visit_BoolOp(self, node):
        """
        Visit a Compare node
        """
        if (node.lineno != self.target_node_lineno):
            return node
        
        if isinstance(node.op, ast.And):
            node.op = ast.Or()
        elif isinstance(node.op, ast.Or):
            node.op = ast.And()
        
        return node

    @classmethod
    def name(cls):
        return 'LOR'  # Logical Operator Replacement


class BitwiseOperatorReplacement(LogicalOperator):

    def visit_BinOp(self, node):
        """
        Visit a Compare node
        """
        if (node.lineno != self.target_node_lineno):
            return node
        
        if isinstance(node.op, ast.BitAnd):
            node.op = ast.BitOr()
        elif isinstance(node.op, ast.BitOr):
            node.op = ast.BitAnd()
        elif isinstance(node.op, ast.BitXor):
            node.op = ast.BitAnd()
        elif isinstance(node.op, ast.LShift):
            node.op = ast.RShift()
        elif isinstance(node.op, ast.RShift):
            node.op = ast.LShift()
        return node

    @classmethod
    def name(cls):
        return 'BOR'  # Bitwise Operator Replacement


class UnaryOperatorDeletion(LogicalOperator):
    def visit_UnaryOp(self, node):
        """
        Visit a Compare node
        """
        if (node.lineno != self.target_node_lineno):
            return node
        
        # if isinstance(node.op, ast.Not):
        #     # return None
        #     # delattr(node, 'op')
        #     node.op = ast.Nonlocal()
        # elif isinstance(node.op, ast.USub):
        #     delattr(node, 'op')
        return node.operand   # very important and tricky, you return only the operand without the operator

    @classmethod
    def name(cls):
        return 'UOR'  # Unary Operator Replacement


# class MembershipOperatorReplacement(LogicalOperator):
#     def visit_Compare(self, node):
#         """
#         Visit a Compare node
#         """
#         if (node.lineno != self.target_node_lineno):
#             return node
        
#         if isinstance(node.ops[0], ast.In):
#             node.ops[0] = ast.NotIn()
#         elif isinstance(node.ops[0], ast.NotIn):
#             node.ops[0] = ast.In()
#         return node

#     @classmethod
#     def name(cls):
#         return 'MR'  # Comparison Operator Replacement


