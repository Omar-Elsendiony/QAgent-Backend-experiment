
import ast
from .base import baseOperator



class OneIterationLoop(baseOperator):

    def one_iteration(self, node):
        node.body.append(ast.Break(lineno=node.body[-1].lineno + 1))
        return node

    def visit_For(self, node):
        if (not self.wanted_line(node.lineno)):
            return node
        return self.one_iteration(node)

    def visit_While(self, node):
        if (not self.wanted_line(node.lineno)):
            return node
        return self.one_iteration(node)

    @classmethod
    def name(cls):
        return 'OIL'  # One Iteration Loop


class ReverseIterationLoop(baseOperator):
    def visit_For(self, node):
        if (not self.wanted_line(node.lineno)):
            return node
        old_iter = node.iter
        node.iter = ast.Call(
            func=ast.Name(id=reversed.__name__, ctx=ast.Load()),
            args=[old_iter],
            keywords=[],
            starargs=None,
            kwargs=None,
        )
        return node

    @classmethod
    def name(cls):
        return 'RIL'  # Reverse Iteration Loop

class ZeroIterationLoop(baseOperator):

    def zero_iteration(self, node):
        node.body = [ast.Break(lineno=node.body[0].lineno)]
        return node

    def visit_For(self, node):
        if (not self.wanted_line(node.lineno)):
            return node
        return self.zero_iteration(node)

    def visit_While(self, node):
        if (not self.wanted_line(node.lineno)):
            return node
        return self.zero_iteration(node)

    @classmethod
    def name(cls):
        return 'ZIL'  # Zero Iteration Loop

class LoopDeletion(baseOperator):

    def visit_While(self, node):
        if not self.wanted_line(node.lineno):
            return node
        return None

    def visit_For(self, node):
        if not self.wanted_line(node.lineno):
            return node
        return None

    @classmethod
    def name(cls):
        return 'LOD'  # Statement Deletion
