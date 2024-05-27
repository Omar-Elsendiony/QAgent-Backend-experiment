"""
Module Description:
Module entails all the classes that are involved in the mutation of arithmetic operators in the code
These includes:
- BinOp: Binary operators that are infix operators
- UnaryOp: Unary operators that are prefix operators
- Mult: Multiplication operator
- Div: Division operator
- Mod: Modulus operator
- Pow: Power operator
- LShift: Left shift operator
- RShift: Right shift operator

"""
import ast
from .base import baseOperator

class ArithmeticOperator(baseOperator):
    """
    Base Class for all arithmetic operators
    Inherits from Node transformer
    """
    @property
    def lineno(self):
        return self.target_node_lineno

    @lineno.setter
    def lineno(self, lineno):
        self.target_node_lineno = lineno

    @classmethod
    def printMutatedSet(cls):
        print(cls.mutatedSet)

    @classmethod
    def name(cls):
        return 'AR' # Arithmetic short form

class ArithmeticOperatorDeletion(ArithmeticOperator):
    # def get_operator_type(self):
    #     return ast.UAdd, ast.USub

    # def visit_UnaryOp(self, node):
    #     """
    #     Unary operators talk
    #     """
    #     if isinstance(node.op, self.get_operator_type()):
    #         return node.operand
    #     return self.generic_visit(node)
    

    def visit_BinOp(self, node):
        """
        function targets the addition and subtraction operators that are considered infix operators
        """
        if self.wanted_line(node.lineno):
            self.finishedMutation = True
            # self.mutatedSet.add(node)
            return self.visit(node.left)
        else:
            return ast.BinOp(left = self.visit(node.left), op=node.op, right=self.visit(node.right)) # if you do not want to continue visiting child nodes, if not self.generic_visit(node)

    @classmethod
    def name(cls):
        return 'ARD' # Arithmetic short form for deletion

class AdditionOperatorReplacement(ArithmeticOperator):

    # def visit_BinOp(self, node):
    #     """
    #     function targets the addition and subtraction operators that are considered infix operators
    #     """
    #     if self.wanted_line(node.lineno, node.col_offset):
    #         self.finishedMutation = True
    #         self.mutatedSet.add(node)
    #         return ast.BinOp(left=self.visit(node.left), op=ast.Sub(), right=self.visit(node.right))
    #     else:
    #         return node # if you do not want to continue visiting child nodes, if not self.generic_visit(node)

    @classmethod
    def name(cls):
        return 'ADD' # Arithmetic replacement short form

    def visit_Add(self, node):
        if node.parent is not None and self.wanted_line(node.parent.lineno, '+'):
            self.finishedMutation = True
            # self.mutatedSet.add(node)
            return ast.Sub()
        return node

class SubtractionOperatorReplacement(ArithmeticOperator):

    # def visit_BinOp(self, node):
    #     """
    #     function targets the addition and subtraction operators that are considered infix operators
    #     """
    #     if self.wanted_line(node.lineno, '-'):
    #         self.finishedMutation = True
    #         self.mutatedSet.add(node)
    #         return ast.BinOp(left=self.visit(node.left), op=ast.Add(), right=self.visit(node.right))
    #     else:
    #         return node # if you do not want to continue visiting child nodes, if not self.generic_visit(node)

    @classmethod
    def name(cls):
        return 'SUB' # Arithmetic replacement short form



    def visit_Sub(self, node):
        if node.parent is not None and self.wanted_line(node.parent.lineno, '-'):
            self.finishedMutation = True
            # self.mutatedSet.add(node)
            return ast.Add()
        return node

class MultiplicationOperatorReplacement(ArithmeticOperator):

    # By default it calls the __init__ method of the parent class so, it is redundant to define it again
    # and we do not want to add any logic or whatsoever to it
    mutations = [ast.Div(), ast.Pow()] # list of mutations that can be performed on the node that represents multiplication

    # def visit_BinOp(self, node):
    #     """
    #     function targets the addition and subtraction operators that are considered infix operators
    #     """

    #     if self.wanted_line(node.lineno, node.col_offset):
    #         self.finishedMutation = True
    #         self.mutatedSet.add(node)
    #         mutation = self.choose_mutation_random_dist(MultiplicationOperatorReplacement.mutations)
    #         return ast.BinOp(left = self.visit(node.left), op=mutation, right=self.visit(node.right))
    #     else:
    #         return node # if you do not want to continue visiting child nodes, if not self.generic_visit(node)


    @classmethod
    def name(cls):
        return 'MUL' # Multiplication short form

    def visit_Mult(self, node):
        if node.parent is not None and self.wanted_line(node.parent.lineno, '*'):
            self.finishedMutation = True
            # self.mutatedSet.add(node)
            return ast.Div()
        return node


class DivisionOperatorReplacement(ArithmeticOperator):
    mutations = [ast.Mult(), ast.FloorDiv()]

    # def visit_BinOp(self, node):
    #     """
    #     function targets the addition and subtraction operators that are considered infix operators
    #     """
    #     if self.wanted_line(node.lineno, '/'):
    #         self.finishedMutation = True
    #         self.mutatedSet.add(node)
    #         mutation = self.choose_mutation_random_dist(DivisionOperatorReplacement.mutations)
    #         return ast.BinOp(left=self.visit(node.left), op=mutation, right=self.visit(node.right))
    #     else:
    #         return node # if you do not want to continue visiting child nodes, if not self.generic_visit(node)


    @classmethod
    def name(cls):
        return 'DIV' # Division short form

    def visit_Div(self, node):
        if node.parent is not None and self.wanted_line(node.parent.lineno, '/'):
            self.finishedMutation = True
            # self.mutatedSet.add(node)
            return ast.Mult()
        return node


class FloorDivisionOperatorReplacement(ArithmeticOperator):
    mutations = [ast.Div(), ast.Mod()]

    # def visit_BinOp(self, node):
    #         """
    #         function targets the addition and subtraction operators that are considered infix operators
    #         """
    #         if self.wanted_line(node.lineno, node.col_offset):
    #             self.finishedMutation = True
    #             self.mutatedSet.add(node)
    #             mutation = self.choose_mutation_random_dist(FloorDivisionOperatorReplacement.mutations)
    #             return ast.BinOp(left=self.visit(node.left), op=mutation, right=self.visit(node.right))
    #         else:
    #             return node # if you do not want to continue visiting child nodes, if not self.generic_visit(node)


    @classmethod
    def name(cls):
        return 'FLOORDIV' # Division short form

    def visit_FloorDiv(self, node):
        if node.parent is not None and self.wanted_line(node.parent.lineno, '//'):
            self.finishedMutation = True
            # self.mutatedSet.add(node)
            return ast.Div()
        return node
    

class ModuloOperatorReplacement(ArithmeticOperator):
    mutations = [ast.Div(), ast.FloorDiv()]

    # def visit_BinOp(self, node):
    #         """
    #         function targets the modulo operator to change it if it is in the specified line number
    #         """
    #         if self.wanted_line(node.lineno, node.col_offset):
    #             self.finishedMutation = True
    #             self.mutatedSet.add(node)
    #             mutation = self.choose_mutation_random_dist(ModuloOperatorReplacement.mutations)
    #             return ast.BinOp(left=self.visit(node.left), op=mutation, right=self.visit(node.right))
    #         else:
    #             return node # if you do not want to continue visiting child nodes, if not self.generic_visit(node)




    @classmethod
    def name(cls):
        return 'MOD' # Division short form

    def visit_Mod(self, node):
        if node.parent is not None and self.wanted_line(node.parent.lineno, '%'):
            self.finishedMutation = True
            # self.mutatedSet.add(node)
            return ast.Div()
        return node

class PowerOperatorReplacement(ArithmeticOperator):
    mutations = [ast.Mult()]

    # def visit_BinOp(self, node):
    #     # print(node.op)
    #     if self.wanted_line(node.lineno, node.col_offset):
    #         self.finishedMutation = True
    #         self.mutatedSet.add(node)
    #         mutation = self.choose_mutation_random_dist(PowerOperatorReplacement.mutations)
    #         return ast.BinOp(left = self.visit(node.left), op = mutation, right = self.visit(node.right))
    #     else:
    #         # return node # if you do not want to continue visiting child nodes, if not self.generic_visit(node)
    #         return ast.BinOp(left = self.visit(node.left), op = node.op, right = self.visit(node.right))

    @classmethod
    def name(cls):
        return 'POW' # Division short form

    def visit_Pow(self, node):
        if node.parent is not None and self.wanted_line(node.parent.lineno, '**'):
            self.finishedMutation = True
            # self.mutatedSet.add(node)
            return ast.Mult()
        return node


class UnaryOperator(ast.NodeTransformer):
    pass
    

class AugmentedAssignReplacement(ArithmeticOperator):
    mutations = [ast.BitXor(), ast.Add(), ast.Sub(), ast.Mult(), ast.Div(), ast.FloorDiv(), ast.Mod(), ast.Pow(), ast.BitAnd(), ast.BitOr(), ast.LShift(), ast.RShift()]

    def visit_AugAssign(self, node):
        lineno = getattr(node, 'lineno', None)
        if (lineno is None): parent = getattr(node, 'parent', None); lineno = getattr(parent, 'lineno', None)
        if self.wanted_line(lineno):
            self.finishedMutation = True
            # self.mutatedSet.add(node)
            mutation = self.choose_mutation_random_dist(AugmentedAssignReplacement.mutations)
            return ast.AugAssign(target=self.visit(node.target), op=mutation, value=self.visit(node.value))
        else:
            return node
    
        

    @classmethod
    def name(cls):
        return 'AUG' # Division short form
