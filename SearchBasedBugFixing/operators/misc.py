import ast
from .base import baseOperator
from typing import Any
import random


class BreakContinueReplacement(baseOperator):
    def visit_Break(self, node):
        if not self.wanted_line(node.lineno):
            return node
        return ast.Continue()

    def visit_Continue(self, node):
        if not self.wanted_line(node.lineno):
            return node
        return ast.Break()


    @classmethod
    def name(cls):
        return 'BCR'  # Break Continue Replacement


class SliceIndexRemove(baseOperator):
    def visit_Subscript(self, node):
        if not self.wanted_line(node.lineno):
            return node
        random_choice = random.randint(0, 2)
        if (random_choice == 0):
            return node.value
        return ast.Subscript(value=node.value, slice=self.visit(node.slice), ctx=node.ctx)
    

    def mutate_Slice_remove_lower(self, node):
        return ast.Slice(lower=None, upper=node.upper, step=node.step)

    def mutate_Slice_remove_upper(self, node):
        return ast.Slice(lower=node.lower, upper=None, step=node.step)

    def mutate_Slice_remove_step(self, node):
        return ast.Slice(lower=node.lower, upper=node.upper, step=None)
    
    def visit_Slice(self, node):
        if not self.wanted_line(node.lineno):
            return node
        func = self.choose_mutation_random_dist([self.mutate_Slice_remove_lower, self.mutate_Slice_remove_upper, self.mutate_Slice_remove_step])
        return func(node)

    @classmethod
    def name(cls):
        return 'SIR'  # Slice Index Remove
    
class StatementDeletion(baseOperator):
    """
    Delete 
    """
    def visit_Assign(self, node):
        return ast.Pass()

    def visit_Return(self, node):
        return ast.Pass()

    def visit_Expr(self, node):
        # if utils.is_docstring(node.value):
        #     raise MutationResign()
        return ast.Pass()

    @classmethod
    def name(cls):
        return 'STD' # Statement Deletion



class MembershipReplacement(baseOperator):
    """
    Membership replacement for the members: 
    is
    is not
    in
    not in
    """

    # def visit_Compare(self, node: ast.Compare) -> Any:
    #     if not self.wanted_line(node.lineno):
    #         return node

    #     if isinstance(node.ops[0], ast.Is):
    #         operation = ast.IsNot()
    #     elif isinstance(node.ops[0], ast.IsNot):
    #         operation = ast.Is()
    #     elif isinstance(node.ops[0], ast.In):
    #         operation = ast.NotIn()
    #     elif isinstance(node.ops[0], ast.NotIn):
    #         operation = ast.In()
    #     elif isinstance(node.ops[0], ast.Eq):
    #         # choice
    #         operation = ast.NotEq()
    #     elif isinstance(node.ops[0], ast.NotEq):
    #         operation = ast.Eq()
    #     return ast.Compare(left=self.visit(node.left), ops=[operation], comparators=[self.visit(x) for x in node.comparators])
        # return super().visit_Compare(node)

    # def visit_Is(self, node: ast.Is) -> Any:
    #     if not self.wanted_line(node.lineno, node.col_offset):
    #         return node
    #     return ast.IsNot()

    # def visit_IsNot(self, node: ast.IsNot):
    #     if not self.wanted_line(node.lineno, node.col_offset):
    #         return node
    #     return ast.Is()

    # not IN removed for Nowwwwwwwwwwwww
    
    def visit_Eq(self, node: ast.Eq):
        if not self.wanted_line(node.parent.lineno):
            return node
        operations = [ast.NotEq(), ast.LtE(), ast.GtE()]
        op = random.choices(operations, [1, 1, 1], k=1)[0]
        # print(op)
        return op

    # def visit_NotIn(self, node: ast.NotIn):
    #     if not self.wanted_line(node.lineno, node.col_offset):
    #         return node
    #     return ast.In()

    # def visit_In(self, node: ast.In) -> Any:
    #     if not self.wanted_line(node.lineno, node.col_offset):
    #         return node
    #     return ast.NotIn()

    @classmethod
    def name(cls):
        return 'MER'  # Statement Deletion

class ConstantNumericReplacement(baseOperator):

    def is_docstring(node):
        def_node = node.parent.parent
        return (isinstance(def_node, (ast.FunctionDef, ast.ClassDef, ast.Module)) and def_node.body and
                isinstance(def_node.body[0], ast.Expr) and isinstance(def_node.body[0].value, ast.Str) and
                def_node.body[0].value == node)

    def mutate_Num_zero(self, node):
        if not node.n:
            raise node

        return ast.Constant(n=0)
    
    def mutate_Num_one(self, node):
        if not node.n:
            raise node

        return ast.Constant(n=1)
    
    def mutate_Num_minus_one(self, node):
        if not node.n:
            raise node

        return ast.Constant(n=-1)

    
    def mutate_Num_incr_1(self, node):
        return ast.Constant(n=node.n + 1)
    
    def mutate_Num_decr_1(self, node):
        return ast.Constant(n=node.n - 1)


    def visit_Constant(self, node):
        if isinstance(node.n, str):
            return node
        if not self.wanted_line(node.lineno):
            return node
        func = self.choose_mutation_random_dist([self.mutate_Num_incr_1, self.mutate_Num_decr_1])
        self.finishedMutation = True
        # self.mutatedSet.add(node)
        return func(node)

    @classmethod
    def name(cls):
        return 'CNR'  # Constant Replacement

class ConstantStringReplacement(baseOperator):

    def visit_Str(self, node):
        if not self.wanted_line(node.lineno):
            return node
        return ast.Constant(s='')

    @classmethod
    def name(cls):
        return 'CSR'  # Constant Replacement

class returnReplacement(baseOperator):
    def visit_Return(self, node):
        if not self.wanted_line(node.lineno):
            return node
        p = s = a = ast.Pass()
        if (node.value is not None):
            s = ast.BinOp(left=node.value, op=ast.Sub(), right=ast.Constant(value=1))
            a = ast.BinOp(left=node.value, op=ast.Add(), right=ast.Constant(value=1))
        valueChosen = random.choice([s, a, p])
        
        # valueChosen = random.choice([s, a, p])
        # else:  
        #     valueChosen = None
        if valueChosen == p:
            return ast.Return()
        return ast.Return(value=valueChosen)

    @classmethod
    def name(cls):
        return 'RER'  # Return Replacement
    
