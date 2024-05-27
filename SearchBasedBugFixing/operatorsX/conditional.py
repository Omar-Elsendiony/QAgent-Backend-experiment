
import ast
from .base import baseOperator


class ConditionalOperatorInsertion(baseOperator):
    """
    Class that is very unique to the project.
    it negates the condition of the target node
    The negation is in the relational operator
    """
    def negate_test(self, node):
        not_node = ast.UnaryOp(op=ast.Not(), operand=node.test)
        node.test = not_node
        return node

    def visit_While(self, node):
        if (node.lineno != self.target_node_lineno):
            return node
        return self.negate_test(node)

    def visit_If(self, node):
        if (node.lineno != self.target_node_lineno):
            return node
        return self.negate_test(node)

    # def mutate_In(self, node):
    #     if (node.lineno != self.target_node_lineno):
    #         return node
    #     return ast.NotIn()

    # def mutate_NotIn(self, node):
    #     if (node.lineno != self.target_node_lineno):
    #         return node
    #     return ast.In()
    
    @classmethod
    def name(cls):
        return 'COI'  # Conditional Operator Insertion

class ConditionalDeletion(baseOperator):
    def visit_If(self, node):
        if not self.wanted_line(node.lineno):
            return node
        # remove the second branch of the if statement
        # node.orelse = []
        # delete either the if or the else branch

        # roll dice and choose to either delete the entire if statement or only the else branch
        # you may remove the condition or the entire if statement
        import random
        rand = random.randint(0, 1)
        if rand == 0:
            return None
        else: # focus, this may be changed drastically
            # return (ast.IfExp(test=self.visit(node.test), body=self.visit(node.body), orelse=None), node)
            return node.body
        
        return None


    @classmethod
    def name(cls):
        return 'COD'  # Statement Deletion
